import cmath
from src.data_type import Measurement
from src.data_compressor.compressor import Compressor
from .compress_apca_ft import CompressAPCAFT

# paper
# APCA FFT - Adaptive Piecewise Constant Approximation based on FFT
# OBST2013.pdf
class CompressAPCAFFT(Compressor):

  PI = 3.14159265359

  def __init__(self, config = {}) -> None:
    super().__init__()
    compress_ratio = config.get('compress_ratio', 0.5)
    self.config = {
      'compress_ratio': compress_ratio
    }
    self.compressor = CompressAPCAFT()
    self.compressor.set_ft_function(self._ft_function)
     
  def _ft_function(self, x):
    N = len(x)
    if N <= 1: 
      return x
    even = self._ft_function(x[0::2])
    odd = self._ft_function(x[1::2])
    T = []
    for k in range(N//2):
      currnet_value = odd[k] if k < len(odd) else 0
      T.append(cmath.exp(2j*self.PI*k/N)* currnet_value)
    part_a = []
    part_b = []
    for k in range(N//2):
      currnet_value = even[k] if k < len(even) else 0
      part_a.append(T[k] + currnet_value)
      part_b.append(T[k] - currnet_value)
    return part_a + part_b

  def compress(self): 
    self.compressor.config = self.config
    self.compressor.original_data = self.original_data
    self.compressor.compressed_data = self.compressed_data
    self.compressor.compress()
    for measurement in self.compressor.compressed_data:
      measurement.value = measurement.value.real
