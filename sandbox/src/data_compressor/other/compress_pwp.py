import random
from src.data_compressor.compressor import Compressor

# custom
# Pick With Probability
class CompressPWP(Compressor):

  def __init__(self) -> None:
    super().__init__()
    self.config = {
      'probability': 0.5
    }

  def _get_with_probability(self, probablity: int):
    return random.randint(0, 100) < probablity

  def compress(self):
    probablity = int(self.config['probability'] * 100)
    data_len = len(self.original_data)
    if data_len < 1:
      self.compressed_data = self.original_data
      return
    first_measurement = self.original_data[0]
    last_measurement = self.original_data[data_len - 1]
    self.compressed_data.append(first_measurement)
    for i in range(1, data_len):
      if self._get_with_probability(probablity):
        self.compressed_data.append(self.original_data[i])
    if self.compressed_data[len(self.compressed_data) - 1].timestamp != last_measurement.timestamp:
      self.compressed_data.append(last_measurement)
