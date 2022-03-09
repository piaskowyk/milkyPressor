from src.data_compressor.compressor import Compressor

class CompressMinMax(Compressor):

  config = {
    'points_count': 30,
    'points_part': 0.5,
    'use_points_count': False
  }

  def compress(self):
    if len(self.original_data) == 0:
      return
    config = self.config
    if config['use_points_count']:
      points_count = config['points_count']
    else:
      points_count = round(len(self.original_data) * config['points_part'])
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
      measurements.remove(min_measurement)
      measurements.remove(max_measurement)
      compressed_measurements_set.add(min_measurement)
      compressed_measurements_set.add(max_measurement)
    self.compressed_data = sorted(compressed_measurements_set, key=lambda measurement: measurement.timestamp)
