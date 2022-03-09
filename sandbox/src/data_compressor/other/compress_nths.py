from src.data_compressor.compressor import Compressor

class CompressNTHS(Compressor):

  config = {
    'n': 3
  }

  def compress(self):
    data_len = len(self.original_data)
    for i in range(0, data_len, self.config['n']):
      self.compressed_data.append(self.original_data[i])
    if data_len % 3 != 0:
      self.compressed_data.append(self.original_data[data_len - 1])
    return self.compressed_data
