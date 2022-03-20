from src.data_compressor.compressor import Compressor

# STC - Piecewise Linear Representation of Time Series based on Slope Change Threshold
# 1-s2.0-S1875389212006219-main
class CompressSTC(Compressor):

  def __init__(self) -> None:
    super().__init__()
    self.config = {
      'slope_angle': 0.4
    }

  def compress(self):
    if len(self.original_data) == 0:
      return
    if len(self.original_data) < 4:
      self.compressed_data = self.original_data
    slope_angle_d = self.config['slope_angle']

    output = [self.original_data[0]]
    for i in range(2, len(self.original_data)):
      point_a = self.original_data[i - 2]
      point_b = self.original_data[i - 1]
      point_c = self.original_data[i]
      slope_angel_ab = (point_b.value - point_a.value) / (point_b.timestamp - point_a.timestamp)
      slope_angel_cb = (point_c.value - point_b.value) / (point_c.timestamp - point_b.timestamp)
      ratio = abs(slope_angel_ab / slope_angel_cb - 1)
      if ratio > slope_angle_d:
        output.append(point_b)
        output.append(point_c)

    if output[len(output) - 1].timestamp != self.original_data[len(self.original_data) - 1].timestamp:
      output.append(self.original_data[len(self.original_data) - 1])
    self.compressed_data = output
