import cmath
from typing import Callable, List
from src.data_type import Measurement
from src.data_compressor.compressor import Compressor

# paper
# APCA DFT - Adaptive Piecewise Constant Approximation based on FT
# OBST2013.pdf
class CompressAPCAFT(Compressor):

  config = {
    'compress_ratio': 0.5
  }
  
  PI = 3.14159265359

  ft_function: Callable[[list[float]], float]  = lambda data: 1

  def set_ft_function(self, ft_function: Callable[[list[float]], float]):
    self.ft_function = ft_function

  def _call_ft_function(self, data: list[float]) -> float:
    return self.ft_function(data)
  
  def _get_peaks(self, data):
    data_count = len(data)
    out = [0, data_count - 1]
    last_value = 0j
    for i in range(1, data_count, 3):
      if data[i].real > 0:
        if last_value.real > data[i].real:
          out.append(i)
      else:
        if last_value.real < data[i].real:
          out.append(i)
      last_value = data[i]
    return out

  def _get_main_frequencies(self, dft_data, points_count_limit):
    mid_point = len(dft_data)//2
    frequencies = dft_data[:mid_point]
    main_frequencies = []
    for _ in range(mid_point):
      max_index = 0
      max_value = 0
      for index, frequency in enumerate(frequencies):
        if abs(frequency) > abs(max_value):
          max_value = frequency
          max_index = index
      main_frequencies.append((max_index, max_value))
      frequencies[max_index] = 0
      points_count_limit -= frequency.real
      if points_count_limit <= 0:
        break
    return main_frequencies

  def compress(self): 
    data_count = len(self.original_data)
    if data_count < 1:
      self.compressed_data = self.original_data
      return
    points_count_limit = self.config['compress_ratio'] * data_count

    first_timestamp = self.original_data[0].timestamp
    last_timestamp = self.original_data[data_count - 1].timestamp
    points_x = set()
    frequency_series = []
    values = [measurement.value for measurement in self.original_data]
    dft = self._call_ft_function(values)
    frequencies = self._get_main_frequencies(dft, points_count_limit)
    for frequency, amplitude in frequencies:
      data = [2 * amplitude * cmath.exp(2j * self.PI * i * frequency / data_count) for i in range(data_count)]
      frequency_series.append(data)
      peaks = self._get_peaks(data)
      if points_count_limit > len(points_x):
        for peak_x in peaks:
          points_x.add(peak_x)
      else:
        break
    duration = last_timestamp - first_timestamp
    for key in sorted(list(points_x)):
      value = 0
      for line in frequency_series:
        value += line[key]
      value /= data_count
      timestamp = first_timestamp + duration * (key / data_count)
      self.compressed_data.append(Measurement(value, timestamp))
