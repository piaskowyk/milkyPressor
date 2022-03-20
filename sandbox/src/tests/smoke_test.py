import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparent = os.path.dirname(parentdir)
sys.path.append(grandparent)


from src.signal_generator import SignalGenerator
from src.metrics import Metric
from src.data_type import Measurement
from src.data_compressor.other import CompressNTHS
from src.data_compressor.other import CompressMinMax
from src.data_compressor.other import CompressPWP
from src.data_compressor.pip import CompressPIP_ED
from src.data_compressor.pip import CompressPIP_PD
from src.data_compressor.pip import CompressPIP_VD
from src.data_compressor.paa import CompressPAA
from src.data_compressor.paa import CompressPAAVI
from src.data_compressor.paa import CompressByChunk
from src.data_compressor.pla import CompressAPCADFT
from src.data_compressor.pla import CompressAPCAFFT
from src.data_compressor.pla import CompressSTC
from src.data_compressor.pla import CompressHigherDeriveration

signal_generator = SignalGenerator(0, 100).with_peaks(3).with_peaks(3, direction=-1).sin(0.2, 0.2)
measurements = [Measurement(measurement, index * 100) for index, measurement in enumerate(signal_generator.data)]

compression_methods = [
  CompressNTHS(),
  CompressMinMax(),
  CompressPWP(),
  CompressPIP_ED(),
  CompressPIP_PD(),
  CompressPIP_VD(),
  CompressPAA(),
  CompressPAAVI(),
  CompressByChunk(),
  CompressAPCADFT(),
  CompressAPCAFFT(),
  CompressSTC(),
  CompressHigherDeriveration()
]

for data_compressor in compression_methods:
  measurements_ = [Measurement(measurement.value, measurement.timestamp) for measurement in measurements]
  data_compressor.set_data(measurements_)
  data_compressor.compress()
  print(data_compressor.get_stats())
