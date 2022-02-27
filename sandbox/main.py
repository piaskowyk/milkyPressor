from src.signal_generator import SignalGenerator
from src.metrics import Metric
from src.data_type import Measurement

from src.data_compressor.custom import CompressNTHS

signal_generator = SignalGenerator(0, 100).with_peaks(3).with_peaks(3, direction=-1).sin(0.2, 0.2)
measurements = [Measurement(measurement, index * 100) for index, measurement in enumerate(signal_generator.data)]

data_compressor = CompressNTHS()
data_compressor.set_data(measurements)
data_compressor.compress()
data_compressor.get_stats()
data_compressor.vizualize(True, True)
