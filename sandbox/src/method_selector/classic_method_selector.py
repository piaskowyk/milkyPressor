from src.data_compressor.compressors_provider import CompressorsProvider
from src.metric import ComparationMetric
from src.data_type import Measurement
from src.data_compressor.compressor import Compressor
from typing import List, Dict
from collections import defaultdict as dict

class ClassicMethodSelector:

  def __init__(self) -> None:
    self.comparation_metrics_containter = ComparationMetric()
    self.metrics = None
    self.compressors: Dict[str, Compressor] = CompressorsProvider.get_compressors()

  def set_metrics(self, metrics):
    self.metrics = metrics

  def print_result(self, metric_result):
    for key, metrics in metric_result.items():
      print(key)
      for name, value in metrics.items():
        print(f"\t{name}:\t{value}")

  def get_best(self, data: List[Measurement]):
    metric_result = dict()
    for name, compressor in self.compressors.items():
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      metric_result[name] = self.comparation_metrics_containter.compute_metrics(data, compressed_data, self.metrics)
      # self.print_result(metric_result)
    agregated_metrics = dict()
    for method_name, metrics_value in metric_result.items():
      agregated_metrics[method_name] = sum(metrics_value.values())
    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: -item[1])
    best_method_name, _ = sorted_methods[0]
    return best_method_name
