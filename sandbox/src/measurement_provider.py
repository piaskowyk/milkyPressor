from src.signal_generator import SignalGenerator
from src.data_type import Measurement
from src.data_type import Measurement
from typing import List
import json

class MeasurementProvider:
  def __init__(self) -> None:
    pass

  def to_measurements(self, signal_generator: SignalGenerator) -> List[Measurement]:
    return [Measurement(measurement, index * 100) for index, measurement in enumerate(signal_generator.data)]

  def strip_data(self, data: List[Measurement]) -> List[float]:
    return [item.value for item in data]

  def get_random1(self) -> List[List[Measurement]]:
    signal_generators = [
      SignalGenerator(0, 100).with_peaks(3).with_peaks(3, direction=-1).sin(0.2, 0.2),
      SignalGenerator(0, 100).with_peaks(3).with_peaks(3, direction=-1).noise(),
      SignalGenerator(0, 100).with_peaks(3).noise(),
      SignalGenerator(0, 100).with_peaks(3),
      SignalGenerator(0, 100).square_vawe(),
      SignalGenerator(0, 100).square_vawe().with_peaks(5),
      SignalGenerator(0, 100).square_vawe().with_peaks(5).sin(),
      SignalGenerator(0, 100).square_vawe().with_peaks(5).sin().noise(),
      SignalGenerator(0, 100).square_vawe().with_peaks(5).sin(100).noise(),
      SignalGenerator(0, 100).square_vawe().with_peaks(50).noise(),
    ]
    return [self.to_measurements(signal_generator) for signal_generator in signal_generators]

  def json_to_measurements(self, path: str):
    result = []
    with open(f'../datasets/parsed/{path}', 'r') as file:
      json_object = json.load(file)
    for item in json_object:
      result.append(Measurement(item['value'], item['timestamp']))
    return result
