import math
from src.data_compressor.compressor import Compressor
from src.data_type import Measurement
from .compress_pip import CompressPIP

# paper
# PIP-VD - perceptual interesting points, vertical distance
class CompressPIP_VD(Compressor):

  def __init__(self) -> None:
    super().__init__()
    self.config = {
      'compress_ratio': 0.5
    }
    self.compressor = CompressPIP()
    self.compressor.set_metric(self._vertical_distance)

  def _euqlides_distance(self, point_a: Measurement, point_b: Measurement) -> float:
    return math.sqrt((point_a.timestamp - point_b.timestamp) ** 2 + (point_a.value - point_b.value) ** 2)

  def _interpolate_value(self, x: int, point_A: Measurement, point_B: Measurement) -> float:
    return ((point_B.value - point_A.value) / (point_B.timestamp - point_A.timestamp)) * x \
      + ((point_B.timestamp * point_A.value - point_A.timestamp * point_B.value) / (point_B.timestamp - point_A.timestamp))

  def _vertical_distance(self, point_mid: Measurement, point_a: Measurement, point_b: Measurement) -> float:
    projection_y = self._interpolate_value(point_mid.timestamp, point_a, point_b)
    projection_point = Measurement(projection_y, point_mid.timestamp)
    return self._euqlides_distance(point_mid, projection_point)

  def compress(self):
    self.compressor.config = self.config
    self.compressor.original_data = self.original_data
    self.compressor.compressed_data = self.compressed_data
    self.compressor.compress()
