from src.data_type import Measurement
from src.data_compressor.compressor import Compressor

# custom
class NoCompress(Compressor):

  def __init__(self) -> None:
    super().__init__()

  def compress(self):
    self.compressed_data = [Measurement(item.value, item.timestamp) for item in self.original_data]
