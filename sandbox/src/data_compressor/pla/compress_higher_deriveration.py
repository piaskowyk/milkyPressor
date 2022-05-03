from src.data_compressor.compressor import Compressor

class CompressHigherDeriveration(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    deriveration_factor = config.get('deriveration_factor', 0.3)
    self.config = {
      'deriveration_factor': deriveration_factor
    }

  def compress(self):
    if len(self.original_data) == 0:
      return
    min_value = self.original_data[0].value
    max_value = self.original_data[0].value
    for measurement in self.original_data:
      if measurement.value > max_value:
        max_value = measurement.value
      if measurement.value < min_value:
        min_value = measurement.value
    deriveration = self.config['deriveration_factor']
    last_measurement_value = self.original_data[0].value
    for measurement in self.original_data:
      if abs(last_measurement_value - measurement.value) > deriveration:
        self.compressed_data.append(measurement)
        last_measurement_value = measurement.value