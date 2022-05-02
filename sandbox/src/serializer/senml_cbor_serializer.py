from typing import List
from src.data_type import Measurement
from kpn_senml import *

class SenMLCBORSerializer:
  def serialize(self, measurements: List[Measurement], bn_value: str, n_value: str) -> str:
    pack = SenmlPack(bn_value)
    values = [m.value for m in measurements]
    timestamps = [m.timestamp for m in measurements]
    for i in range(len(values)):
      pack.add(SenmlRecord(n_value, value=values[i], time=timestamps[i]))
    cbor_val = pack.to_cbor()
    return cbor_val
