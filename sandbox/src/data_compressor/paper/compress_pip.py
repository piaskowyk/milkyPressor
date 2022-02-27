import math
import heapq
from src.data_compressor.compressor import Compressor

# PIP - perceptual interesting points
class CompressPIP(Compressor):

  config = {
    'compress_ration': 0.5
  }

  def _euqlides_distance(self, point_a: tuple[int, float], point_b: tuple[int, float]) -> float:
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)

  def compress_pip(self): 
    config = self.config
    points_count = config['compress_ration'] * len(self.original_data)
    last_index = len(self.original_data) - 1
    indexes = [0, last_index]
    heap = []
    heapq.heappush(heap, (-len(self.original_data), 0, last_index))
    
    while len(heap) != 0 and len(indexes) < points_count:
      _, index_start, index_end = heapq.heappop(heap)
      measurement = self.original_data[index_start]
      point_start = (measurement.timestamp, measurement.value)
      measurement = self.original_data[index_end]
      point_end = (measurement.timestamp, measurement.value)
      max_distance_index = index_start
      max_distance = 0
      if index_start + 1 == index_end:
        continue
      for i in range(index_start + 1, index_end):
        measurement = self.original_data[i]
        current_point = (measurement.timestamp, measurement.value)
        distance = self._euqlides_distance(point_start, current_point) + self._euqlides_distance(point_end, current_point)
        if distance > max_distance:
          max_distance = distance
          max_distance_index = i
      indexes.append(max_distance_index)
      heapq.heappush(heap, (-(max_distance_index - index_start), index_start, max_distance_index))
      heapq.heappush(heap, (-(index_end - max_distance_index), max_distance_index, index_end))

    for i in sorted(indexes):
      self.compressed_data.append(self.original_data[i])
