from typing import Callable
import heapq
from src.data_compressor.compressor import Compressor
from src.data_type import Measurement

# paper
# PIP - perceptual interesting points, euqulides distance
class CompressPIP(Compressor):

  config = {
    'compress_ration': 0.5
  }

  metric: Callable[[Measurement, Measurement, Measurement], float]  = lambda point_mid, point_a, point_b: 1

  def set_metric(self, metric: Callable[[Measurement, Measurement, Measurement], float]):
    self.metric = metric

  def _distance_metric(self, point_mid: Measurement, point_a: Measurement, point_b: Measurement) -> float:
    return self.metric(point_mid, point_a, point_b)

  def compress(self): 
    config = self.config
    points_count = config['compress_ration'] * len(self.original_data)
    last_index = len(self.original_data) - 1
    indexes = [0, last_index]
    heap = []
    heapq.heappush(heap, (-len(self.original_data), 0, last_index))
    
    while len(heap) != 0 and len(indexes) < points_count:
      _, index_start, index_end = heapq.heappop(heap)
      point_start = self.original_data[index_start]
      point_end = self.original_data[index_end]
      max_distance_index = index_start
      max_distance = 0
      if index_start + 1 == index_end:
        continue
      for i in range(index_start + 1, index_end):
        measurement = self.original_data[i]
        current_point = Measurement(measurement.value, measurement.timestamp)
        distance = self._distance_metric(current_point, point_start, point_end)
        if distance > max_distance:
          max_distance = distance
          max_distance_index = i
      indexes.append(max_distance_index)
      heapq.heappush(heap, (-(max_distance_index - index_start), index_start, max_distance_index))
      heapq.heappush(heap, (-(index_end - max_distance_index), max_distance_index, index_end))

    for i in sorted(indexes):
      self.compressed_data.append(self.original_data[i])
