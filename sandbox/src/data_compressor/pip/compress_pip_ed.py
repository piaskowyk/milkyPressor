import math
from src.data_compressor.compressor import Compressor
from src.data_type import Measurement
from .compress_pip import CompressPIP

# paper
# PIP-ED - perceptual interesting points, euqulides distance
class CompressPIP_ED(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    compress_ratio = config.get('compress_ratio', 0.5)
    self.config = {
      'compress_ratio': compress_ratio
    }
    self.compressor = CompressPIP()
    self.compressor.set_metric(self._euqlides_distance)

  def _euqlides_distance(self, point_mid: Measurement, point_a: Measurement, point_b: Measurement) -> float:
    return math.sqrt((point_a.timestamp - point_mid.timestamp) ** 2 + (point_a.value - point_mid.value) ** 2) + \
      math.sqrt((point_mid.timestamp - point_b.timestamp) ** 2 + (point_mid.value - point_b.value) ** 2)

  def compress(self):
    self.compressor.config = self.config
    self.compressor.original_data = self.original_data
    self.compressor.compressed_data = self.compressed_data
    self.compressor.compress()
