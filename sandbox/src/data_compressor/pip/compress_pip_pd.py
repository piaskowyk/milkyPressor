from src.data_compressor.compressor import Compressor
from src.data_type import Measurement
from .compress_pip import CompressPIP

# paper
# PIP-PD - perceptual interesting points, perpendicular distance
class CompressPIP_PD(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    compress_ratio = config.get('compress_ratio', 0.5)
    self.config = {
      'compress_ratio': compress_ratio
    }
    self.compressor = CompressPIP()
    self.compressor.set_metric(self._perpendicular_distance)

  def _perpendicular_distance(self, point_mid: Measurement, point_a: Measurement, point_b: Measurement) -> float:
    line_A = (point_b.value - point_a.value) / (point_b.timestamp - point_a.timestamp)
    line_C = (point_b.timestamp * point_a.value - point_a.timestamp * point_b.value) / (point_b.timestamp - point_a.timestamp)
    if line_A == 0:
      return 0
    return abs(line_A * point_mid.timestamp - point_mid.value + line_C) / abs(line_A)

  def compress(self):
    self.compressor.config = self.config
    self.compressor.original_data = self.original_data
    self.compressor.compressed_data = self.compressed_data
    self.compressor.compress()
