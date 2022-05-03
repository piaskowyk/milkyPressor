from src.data_compressor.compressor import Compressor
from src.data_type import Measurement

class CompressByChunk(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    compress_ratio = config.get('compress_ratio', 0.5)
    self.config = {
      'compress_ratio': compress_ratio,
    }

  def compress(self):
    data_size = len(self.original_data)
    chunk_size = int(data_size * self.config['compress_ratio'])
    if chunk_size < 1:
      return
    chunk: list[Measurement] = []
    for index, measurement in enumerate(self.original_data):
      if index != 0 and index % chunk_size == 0:
        value_average = chunk[0].value
        timestamp_average = chunk[0].timestamp
        for chunk_index in range(1, len(chunk)):
          value_average = (value_average + chunk[chunk_index].value) / 2
          timestamp_average = (timestamp_average + chunk[chunk_index].timestamp) / 2
        self.compressed_data.append(Measurement(value_average, round(timestamp_average)))
        chunk = []
      else:
        chunk.append(measurement)
    if len(chunk) != 0:
      for item in chunk:
        value_average = (value_average + item.value) / 2
        timestamp_average = (timestamp_average + item.timestamp) / 2
        self.compressed_data.append(Measurement(value_average, round(timestamp_average)))
