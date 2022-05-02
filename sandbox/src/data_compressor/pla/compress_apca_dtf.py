import cmath
from src.data_compressor.compressor import Compressor
from .compress_apca_ft import CompressAPCAFT

# paper
# APCA DFT - Adaptive Piecewise Constant Approximation based on DFT
# OBST2013.pdf
class CompressAPCADFT(Compressor):

  PI = 3.14159265359

  def __init__(self) -> None:
    super().__init__()
    self.config = {
      'compress_ratio': 0.5
    }
    self.compressor = CompressAPCAFT()
    self.compressor.set_ft_function(self._ft_function)
     
  def _ft_function(self, data):
    N = len(data)
    X = [0 for _ in range(N)]
    for m in range(N):    
      for n in range(N): 
        X[m] += data[n] * cmath.exp(-self.PI * 2j * m * n / N)
    return X

  def compress(self): 
    self.compressor.config = self.config
    self.compressor.original_data = self.original_data
    self.compressor.compressed_data = self.compressed_data
    self.compressor.compress()
    for measurement in self.compressor.compressed_data:
      measurement.value = measurement.value.real
