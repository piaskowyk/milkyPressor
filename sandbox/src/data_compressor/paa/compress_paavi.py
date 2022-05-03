from src.data_compressor.compressor import Compressor
from src.data_type import Measurement

# custom 
# uniform, fixed x interval
# PAA - Piecewise Polynomial Approximation
# kais_2000.pdf https://jmotif.github.io/sax-vsm_site/morea/algorithm/PAA.html
# modification - the better approach for data with variable interval
class CompressPAAVI(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    compress_ratio = config.get('compress_ratio', 0.5)
    self.config = {
      'compress_ratio': compress_ratio,
    }

  def interpolate_value(self, x: int, point_A: Measurement, point_B: Measurement) -> float:
    return ((point_B.value - point_A.value) / (point_B.timestamp - point_A.timestamp)) * x \
      + ((point_B.timestamp * point_A.value - point_A.timestamp * point_B.value) / (point_B.timestamp - point_A.timestamp))

  def compress(self):
    data_size = len(self.original_data)
    if data_size < 2:
      self.compressed_data = self.original_data[:]
      return
    chunk_count = int(data_size * self.config['compress_ratio'])
    x_first = self.original_data[0].timestamp
    x_last = self.original_data[data_size - 1].timestamp

    chunk_size = (x_last - x_first) / chunk_count
    points_per_chunk = int(data_size / chunk_count)
    step_size = chunk_size / points_per_chunk

    series = []
    stop = False
    current_x = x_first
    last_checked_index = 1
    for _ in range(chunk_count):
      current_series = []
      for _ in range(points_per_chunk):
        current_x += step_size
        while current_x > self.original_data[last_checked_index].timestamp:
          last_checked_index += 1
          if last_checked_index >= data_size:
            stop = True
            break
        if stop:
          break
        point_a = self.original_data[last_checked_index - 1]
        point_b = self.original_data[last_checked_index]
        computed_value = self.interpolate_value(current_x, point_a, point_b)
        current_series.append(computed_value)
      if stop:
        break
      series.append(current_series)

    for i, line in enumerate(series):
      value = sum(line) / len(line)
      self.compressed_data.append(Measurement(value, x_first + i * chunk_size))
      self.compressed_data.append(Measurement(value, x_first + (i + 1) * chunk_size))
