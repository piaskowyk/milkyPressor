from calendar import c
import math
from re import S
import matplotlib.pyplot as plt
from typing import Tuple, Any, List
import numpy as np
import statistics
from src.data_type import Measurement

class Metric:

  def _strip_data(self, data: List[Measurement]):
    return [item.value for item in data]

  def _interpolate_points(self, x: int, point_A: Measurement, point_B: Measurement) -> float:
    return ((point_B.value - point_A.value) / (point_B.timestamp - point_A.timestamp)) * x \
      + ((point_B.timestamp * point_A.value - point_A.timestamp * point_B.value) / (point_B.timestamp - point_A.timestamp))

  def _interpolate_data(self, original: List[Measurement], transformed: List[Measurement]):
    interpolated = []
    current_index = 0
    transformed_count = len(transformed)
    data_original_count = len(original)
    if data_original_count < 2:
      return original
    first = original[0]
    if first.timestamp != transformed[0].timestamp:
      interpolated = [Measurement(first.value, first.timestamp)]
      current_index = 1

    data_transformed_count = len(transformed)
    last = original[data_original_count - 1]
    if last.timestamp != transformed[data_transformed_count - 1].timestamp:
      transformed.append(Measurement(last.value, last.timestamp))

    for original_measurement in original:
      for i in range(current_index, transformed_count):
        if transformed[i].timestamp == original_measurement.timestamp:
          interpolated.append(Measurement(original_measurement.value, original_measurement.timestamp))
        elif transformed[i].timestamp < original_measurement.timestamp:
          break
        else:
          current_index = i
      point_a = transformed[i - 1]
      point_b = transformed[i]
      x = original_measurement.timestamp
      y = self._interpolate_points(x, point_a, point_b)
      interpolated.append(Measurement(y, x))
    return interpolated

  def _prepare_data(self, original: List[Measurement], transformed: List[Measurement]):
    return self._strip_data(self._interpolate_data(original, transformed))

  def sum_differences(self, original: List[Measurement], transformed: List[Measurement], use_absolut_value: bool = True) -> float:
    original = self._prepare_data(original, transformed)
    transformed = self._strip_data(transformed)
    differences = [original[i] - transformed[i] for i in range(len(original))]
    if use_absolut_value:
      differences = map(math.fabs, differences)
    return sum(differences)
  
  def arithmetic_average(self, original: List[float], transformed: List[float]) -> float:
    return self.sum_differences(original, transformed) / len(original)

  def standard_derivative(self, original: List[float], transformed: List[float]) -> float:
    n = len(original)
    return math.sqrt(sum([(original[i] - transformed[i])**2 for i in range(n)]) / n)
    
  def function_field(self, original: List[float], transformed: List[float], normalize: bool = True) -> float:
    original_field, transformed_field = np.trapz(original), np.trapz(transformed)
    return math.fabs(original_field - transformed_field) / (max(original_field, transformed_field) if normalize else 1)

  def min(self, original: List[float], transformed: List[float], show_diff: bool = True) -> float:
    if show_diff:
      return min(original) - min(transformed)
    return min(transformed)

  def max(self, original: List[float], transformed: List[float], show_diff: bool = True) -> float:
    if show_diff:
      return max(original) - max(transformed)
    return max(transformed)

  def min_max_diff(self, original: List[float], transformed: List[float], show_diff: bool = True) -> float:
    transformed_diff = abs(max(transformed) - min(transformed))
    if show_diff:
      original_diff = abs(max(original) - min(original))
      return abs(transformed_diff - original_diff)
    return transformed_diff

  def _value_crossing(self, data: List[float], border: float = 0, threshold: float = 0, direction: int = 0) -> float:
    if len(data) == 0:
      return 0

    counter = 0
    lastPosition = None
    position = None

    value = data[0]
    if value > border + threshold:
      lastPosition = 1
    elif value < border - threshold:
      lastPosition = -1
    else:
      lastPosition = 0
      counter = 1

    for value in data:
      if value > border + threshold:
        position = 1
      elif value < border - threshold:
        position = -1
      else:
        position = 0

      if direction == 0:
        if (position == 0 and lastPosition != 0) or (abs(position - lastPosition) == 2):
          counter += 1
      if direction > 0: # positive crossing
        if lastPosition < 0 and position != lastPosition:
          counter += 1
      if direction < 0: # negaive crossing
        if lastPosition > 0 and position != lastPosition:
          counter += 1

    return counter

  def value_crossing(
      self, 
      original: List[float], 
      transformed: List[float], 
      border: float = 0, 
      threshold: float = 0, 
      show_diff: bool = True,
      direction: int = 0
    ) -> float:
    original_cross_count = 0
    transformed_cross_count = self._value_crossing(transformed, border, threshold, direction)
    if show_diff:
      original_cross_count = self._value_crossing(original, border, threshold, direction)
    return transformed_cross_count - original_cross_count

  def positive_value_crossing(
      self, 
      original: List[float], 
      transformed: List[float], 
      border: float = 0, 
      threshold: float = 0, 
      show_diff: bool = True
    ) -> float:
    return self.value_crossing(original, transformed, border, threshold, show_diff, 1)

  def negative_value_crossing(
      self, 
      original: List[float], 
      transformed: List[float], 
      border: float = 0, 
      threshold: float = 0, 
      show_diff: bool = True
    ) -> float:
    return self.value_crossing(original, transformed, border, threshold, show_diff, -1)

  def _peak_detector(
      self, 
      y: List[float], 
      x: List[int] = [], 
      delta: float = 0.3
    ) -> Tuple[Tuple[List[float], List[float]], Tuple[List[float], List[float]]]:
    maxtab = []
    mintab = [] 
    minimum = math.inf
    maximum = -math.inf
    minimum_x = None
    maximum_x = None
    look_for_max = True

    for i in range(len(y)):
        current = y[i]
        if current > maximum:
            maximum = current
            maximum_x = x[i]
        if current < minimum:
            minimum = current
            minimum_x = x[i]
        
        if look_for_max:
            if current < maximum - delta:
                maxtab.append((maximum_x, maximum))
                minimum = current
                minimum_x = x[i]
                look_for_max = False
        else:
            if current > minimum + delta:
                mintab.append((minimum_x, minimum))
                maximum = current
                maximum_x = x[i]
                look_for_max = True

    return [[i[0] for i in maxtab], [i[1] for i in maxtab]], [[i[0] for i in mintab], [i[1] for i in mintab]]

  def peak_count(self, original: List[float], transformed: List[float], delta: float = 0.3, show_diff: bool = True) -> float:
    original_peaks_count = 0
    peaks_positive, peaks_negative = self._peak_detector(transformed, [i for i in range(len(transformed))], delta)
    transformed_peaks_count = len(peaks_positive[0]) + len(peaks_negative[0])
    if show_diff:
      peaks_positive, peaks_negative = self._peak_detector(original, [i for i in range(len(original))], delta)
      original_peaks_count = len(peaks_positive[0]) + len(peaks_negative[0])
    return original_peaks_count - transformed_peaks_count

  def positive_peak_count(self, original: List[float], transformed: List[float], delta: float = 0.3, show_diff: bool = True) -> float:
    original_peaks_count = 0
    peaks_positive, _ = self._peak_detector(transformed, [i for i in range(len(transformed))], delta)
    transformed_peaks_count = len(peaks_positive[0])
    if show_diff:
      peaks_positive, _ = self._peak_detector(original, [i for i in range(len(original))], delta)
      original_peaks_count = len(peaks_positive[0])
    return original_peaks_count - transformed_peaks_count

  def negative_peak_count(self, original: List[float], transformed: List[float], delta: float = 0.3, show_diff: bool = True) -> float:
    original_peaks_count = 0
    _, peaks_negative = self._peak_detector(transformed, [i for i in range(len(transformed))], delta)
    transformed_peaks_count = len(peaks_negative[0])
    if show_diff:
      _, peaks_negative = self._peak_detector(original, [i for i in range(len(original))], delta)
      original_peaks_count = len(peaks_negative[0])
    return original_peaks_count - transformed_peaks_count

  def median(self, original: List[float], transformed: List[float], show_diff: bool = True) -> float:
    if show_diff:
      return statistics.median(original) - statistics.median(transformed)
    return statistics.median(transformed)
  
  def fft(self, transformed: List[float], show_plot: bool = False) -> Tuple[List[float], Any]:
    transformed_np_array = np.array(transformed)
    sp = np.fft.fft(transformed_np_array)
    freq = np.fft.fftfreq(transformed_np_array.shape[-1])
    if show_plot:
      plt.plot(freq, sp.real, freq, sp.imag)
    return sp, freq

  def _mean(self, data: List[float]) -> float:
    return sum(data) / len(data)

  def _covariance(self, x: List[float], y: List[float]) -> float:
    n = len(x)
    mean_x = self._mean(x)
    mean_y = self._mean(y)
    sum_distance = 0
    for i in range(n):
      sum_distance += (x[i] - mean_x) * (y[i] - mean_y)
    return sum_distance * 1/n

  def covariance(self, original: List[float], transformed: List[float], show_diff: bool = True) -> float:
    x_list = [i for i in range(len(transformed))]
    if show_diff:
      return self._covariance(x_list, original) - self._covariance(x_list, transformed)
    return self._covariance(x_list, transformed)

  def _corelation_pearson(self, x: List[float], y: List[float]) -> float:
    mean_x = self._mean(x)
    mean_y = self._mean(y)
    sum_distance = 0
    sum_distance_square_x = 0
    sum_distance_square_y = 0
    for i in range(len(x)):
      distance_x = (x[i] - mean_x)
      distance_y = (y[i] - mean_y)
      sum_distance += distance_x * distance_y
      sum_distance_square_x += distance_x ** 2
      sum_distance_square_y += distance_y ** 2
    return sum_distance / math.sqrt(sum_distance_square_x * sum_distance_square_y)

  def corelation_pearson(self, original: List[float], transformed: List[float], show_diff: bool = True) -> float:
    x_list = [i for i in range(len(transformed))]
    if show_diff:
      return self._corelation_pearson(x_list, original) - self._corelation_pearson(x_list, transformed)
    return self._corelation_pearson(x_list, transformed)

  def _corelation_spearman_on_injection(self, x: List[float], y: List[float]) -> float:
    data_len = len(x)
    n = data_len
    max_rang = data_len
    next_rang = max_rang
    x_rangs = [i + 1 for i in range(max_rang)]
    y_rangs = []
    y_sorted = sorted(y)
    print(y_sorted)
    i = 0
    while i < data_len:
      values_count = 1
      current_value = y[i]
      while i + values_count < data_len and y[i + values_count] == current_value:
        values_count += 1
      current_rang = sum(range(i, i + values_count)) / values_count
      for _ in range(values_count):
        y_rangs.append(current_rang)
      next_rang -= values_count
      i += values_count
    distance_sum = 0
    for i in range(data_len):
      distance_sum += (x_rangs[i] - y_rangs[i]) ** 2
    return 1 - ((6 * distance_sum) / (n * (n ** 2 - 1)))

  def corelation_spearman(self, original: List[float], transformed: List[float], show_diff: bool = True) -> float:
    x_list = [i for i in range(len(transformed))]
    if show_diff:
      return self._corelation_spearman_on_injection(x_list, original) - self._corelation_spearman_on_injection(x_list, transformed)
    return self._corelation_spearman_on_injection(x_list, transformed)

  def compression_ratio(self, original: List[float], transformed: List[float]) -> float:
    return len(transformed) / len(original)
