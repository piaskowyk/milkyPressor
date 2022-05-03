from src.data_compressor.compressor import Compressor

class CompressMinMax(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    if 'compress_ratio' in config:
      compress_ratio = config['compress_ratio']
    else:
      compress_ratio = 0.5
    self.config = {
      'compress_ratio': compress_ratio,
    }

  def compress(self):
    if len(self.original_data) == 0:
      return
    config = self.config
    points_count = round(len(self.original_data) * config['compress_ratio'])
    if points_count < 1:
      return
    compressed_measurements_set = set()
    measurements = set(self.original_data)
    for _ in range(round(points_count / 2)):
      min_measurement = next(iter(measurements))
      max_measurement = next(iter(measurements))
      for measurement in measurements:
        if min_measurement.value > measurement.value:
          min_measurement = measurement
        if max_measurement.value < measurement.value:
          max_measurement = measurement
      if min_measurement in measurements:
        measurements.remove(min_measurement)
      if max_measurement in measurements:
        measurements.remove(max_measurement)
      compressed_measurements_set.add(min_measurement)
      compressed_measurements_set.add(max_measurement)
    self.compressed_data = sorted(compressed_measurements_set, key=lambda measurement: measurement.timestamp)
