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
      'CompressNTHS_0.9': CompressNTHS({'compress_ratio': 0.9}),
      'CompressNTHS_0.8': CompressNTHS({'compress_ratio': 0.8}),
      'CompressNTHS_0.7': CompressNTHS({'compress_ratio': 0.7}),
      'CompressNTHS_0.6': CompressNTHS({'compress_ratio': 0.6}),
      'CompressNTHS_0.5': CompressNTHS({'compress_ratio': 0.5}),
      'CompressNTHS_0.4': CompressNTHS({'compress_ratio': 0.4}),
      'CompressNTHS_0.3': CompressNTHS({'compress_ratio': 0.3}),
      'CompressNTHS_0.2': CompressNTHS({'compress_ratio': 0.2}),
      'CompressNTHS_0.1': CompressNTHS({'compress_ratio': 0.1}),

      'CompressMinMax_0.9': CompressMinMax({'compress_ratio': 0.9}),
      'CompressMinMax_0.8': CompressMinMax({'compress_ratio': 0.8}),
      'CompressMinMax_0.7': CompressMinMax({'compress_ratio': 0.7}),
      'CompressMinMax_0.6': CompressMinMax({'compress_ratio': 0.6}),
      'CompressMinMax_0.5': CompressMinMax({'compress_ratio': 0.5}),
      'CompressMinMax_0.4': CompressMinMax({'compress_ratio': 0.4}),
      'CompressMinMax_0.3': CompressMinMax({'compress_ratio': 0.3}),
      'CompressMinMax_0.2': CompressMinMax({'compress_ratio': 0.2}),
      'CompressMinMax_0.1': CompressMinMax({'compress_ratio': 0.1}),

      'CompressPWP_0.9': CompressPWP({'compress_ratio': 0.9}),
      'CompressPWP_0.8': CompressPWP({'compress_ratio': 0.8}),
      'CompressPWP_0.7': CompressPWP({'compress_ratio': 0.7}),
      'CompressPWP_0.6': CompressPWP({'compress_ratio': 0.6}),
      'CompressPWP_0.5': CompressPWP({'compress_ratio': 0.5}),
      'CompressPWP_0.4': CompressPWP({'compress_ratio': 0.4}),
      'CompressPWP_0.3': CompressPWP({'compress_ratio': 0.3}),
      'CompressPWP_0.2': CompressPWP({'compress_ratio': 0.2}),
      'CompressPWP_0.1': CompressPWP({'compress_ratio': 0.1}),

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