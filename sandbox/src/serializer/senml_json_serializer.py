from typing import List
from src.data_type import Measurement
import json

class SenMLJSONSerializer:
  def serialize(self, measurements: List[Measurement], bn_value: str, n_value: str, metrics: List[float]) -> str:
    output = []
    values = [m.value for m in measurements]
    timestamps = [m.timestamp for m in measurements]
    data_size = len(values)
    index = data_size - 1
    base_time = timestamps[index]
    output.append({
      'bn': bn_value,
      'n': n_value,
      'v': values[index],
      'bt': timestamps[index],
      't': 0
    })
    index -= 1
    while index > -1:
      output.append({
        'n': n_value,
        'v': values[index],
        't': timestamps[index] - base_time,
      })
      index -= 1
    output.append({
      'n': '123',
      'v': metrics,
    })
    return json.dumps(output)
