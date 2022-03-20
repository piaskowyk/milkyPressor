from src.data_compressor.compressor import Compressor

class CompressHigherDeriveration(Compressor):

  def __init__(self) -> None:
    super().__init__()
    self.config = {
      'deriveration': 0.05
    }

  def compress(self):
    deriveration = self.config['deriveration']
    if len(self.original_data) == 0:
      return
    last_measurement_value = self.original_data[0].value
    for measurement in self.original_data:
      if abs(last_measurement_value - measurement.value) > deriveration:
        self.compressed_data.append(measurement)
        last_measurement_value = measurement.value