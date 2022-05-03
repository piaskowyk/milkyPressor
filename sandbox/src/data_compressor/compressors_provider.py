from src.data_compressor.other import CompressNTHS, CompressMinMax, CompressPWP, NoCompress
from src.data_compressor.pip import CompressPIP_ED, CompressPIP_PD, CompressPIP_VD
from src.data_compressor.paa import CompressPAA, CompressPAAVI, CompressByChunk
from src.data_compressor.pla import CompressAPCADFT, CompressAPCAFFT, CompressSTC, CompressHigherDeriveration
from src.data_compressor.compressor import Compressor
from typing import Dict

class CompressorsProvider:

  @staticmethod
  def get_compressors() -> Dict[str, Compressor]:
    compressors = {
      'CompressByChunk': CompressByChunk(),
      'CompressAPCADFT': CompressAPCADFT(),
      'CompressAPCAFFT': CompressAPCAFFT(),
      'CompressSTC': CompressSTC(),
      'CompressHigherDeriveration': CompressHigherDeriveration(),
    }
    generator = [
      ('CompressNTHS', CompressNTHS),
      ('CompressMinMax', CompressMinMax),
      ('CompressPWP', CompressPWP),
      ('CompressPIP_ED', CompressPIP_ED),
      ('CompressPIP_PD', CompressPIP_PD),
      ('CompressPIP_VD', CompressPIP_VD),
      ('CompressPAA', CompressPAA),
      ('CompressPAAVI', CompressPAAVI),
    ]
    for name, class_ in generator:
      for compress_ratio in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        compressors[name] = class_({'compress_ratio': compress_ratio})
    return compressors
  
  @staticmethod
  def get(compressor_name: str) -> Compressor:
    if compressor_name == 'NoCompress':
      return NoCompress()
    return CompressorsProvider.get_compressors()[compressor_name]