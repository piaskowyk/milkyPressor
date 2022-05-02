import matplotlib.pyplot as plt
from src.data_type import Measurement
from typing import List
import os

class Compressor:

  def __init__(self) -> None:
    super().__init__()
    self.original_data: List[Measurement] = []
    self.compressed_data: List[Measurement] = []
    self.config = {}

  def compress(self):
    raise "Unimplement method"

  def push(self, measurement: Measurement):
    self.original_data.append(measurement)
  
  def set_data(self, measurements: List[Measurement]):
    self.original_data = measurements

  def clean_data(self):
    self.original_data = []
    self.compressed_data = []

  def vizualize(self, show_compressed: bool = True, show_interpolation: bool = False, config: any = {}):
    x_original = [measurement.timestamp for measurement in self.original_data]
    y_original = [measurement.value for measurement in self.original_data]
    plt.figure(dpi=100)
    if show_interpolation:
      plt.plot(x_original, y_original, 'b')
    plt.plot(x_original, y_original, 'bo', label='Original data')
    if show_compressed:
      x_compressed = [measurement.timestamp for measurement in self.compressed_data]
      y_compressed = [measurement.value for measurement in self.compressed_data]
      if show_interpolation:
        plt.plot(x_compressed, y_compressed, 'r')
      plt.plot(x_compressed, y_compressed, 'ro', label='Compressed data')
    if 'title' in config:
      plt.title(config['title'])
      plt.xlabel("time [ms]")
      plt.ylabel("measurement value [x]")
      plt.legend(loc="upper right")
    plt.grid()
    if 'dir' in config:
      path = 'images/' + config['dir'] + '/'
      if 'fileName' in config:
        full_path = 'images/' + config['dir'] + '/' + config['fileName'] + '.png'
      else:
        full_path = 'images/' + config['dir'] + '/' + config['title'] + '.png'
      if not os.path.exists(path):
        os.makedirs(path)
      plt.savefig(full_path)
    plt.show()
    return self

  def get_data(self):
    return [measurement.value for measurement in self.compressed_data]

  def get_stats(self):
    return {
      'original_size': len(self.original_data),
      'compressed_size': len(self.compressed_data),
      'compression_rate': (len(self.original_data) - len(self.compressed_data)) / len(self.original_data)
    }