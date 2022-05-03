from src.data_compressor.other import CompressNTHS, CompressMinMax, CompressPWP, NoCompress
from src.data_compressor.pip import CompressPIP_ED, CompressPIP_PD, CompressPIP_VD
from src.data_compressor.paa import CompressPAA, CompressPAAVI, CompressByChunk
from src.data_compressor.pla import CompressAPCADFT, CompressAPCAFFT, CompressSTC, CompressHigherDeriveration
from src.data_compressor.compressor import Compressor
from typing import Dict

class CompressorsProvider:

  @staticmethod
  def get_compressors() -> Dict[str, Compressor]:
    return {
      'CompressNTHS': CompressNTHS(),
      'CompressMinMax': CompressMinMax(),
      'CompressPWP': CompressPWP(),
      'CompressPIP_ED': CompressPIP_ED(),
      'CompressPIP_PD': CompressPIP_PD(),
      'CompressPIP_VD': CompressPIP_VD(),
      'CompressPAA': CompressPAA(),
      'CompressPAAVI': CompressPAAVI(),
      'CompressByChunk': CompressByChunk(),
      'CompressAPCADFT': CompressAPCADFT(),
      'CompressAPCAFFT': CompressAPCAFFT(),
      'CompressSTC': CompressSTC(),
      'CompressHigherDeriveration': CompressHigherDeriveration(),
    }
  
  @staticmethod
  def get(compressor_name: str) -> Compressor:
    if compressor_name == 'NoCompress':
      return NoCompress()
    return CompressorsProvider.get_compressors()[compressor_name]