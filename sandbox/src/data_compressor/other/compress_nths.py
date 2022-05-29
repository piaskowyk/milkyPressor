from src.data_compressor.compressor import Compressor

class CompressNTHS(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    compress_ratio = config.get('compress_ratio', 0.5)
    n = 1 / compress_ratio
    if n == 0:
      n = 1
    self.config = {
      'n': n
    }

  def compress(self):
    data_len = len(self.original_data)
    n = self.config['n']
    current_index = 0
    while current_index < data_len:
      if int(current_index + n) == current_index:
        current_index += n
        if int(current_index) >= data_len:
          break
        continue
      self.compressed_data.append(self.original_data[int(current_index)])
      current_index += n
    if self.original_data[data_len - 1].timestamp != self.compressed_data[len(self.compressed_data) - 1].timestamp:
      self.compressed_data.append(self.original_data[data_len - 1])
    return self.compressed_data
