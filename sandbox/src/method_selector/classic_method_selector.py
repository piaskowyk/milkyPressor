from src.data_compressor.compressors_provider import CompressorsProvider
from ..metric import ComparationMetricEnum
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

  def print_result(self, metric_result) -> None:
    for key, metrics in metric_result.items():
      print(key)
      for name, value in metrics.items():
        print(f"\t{name}:\t{value}")

  def get_best_with_default_strategy(self, data: List[Measurement], comparation_metrics: List[ComparationMetricEnum]) -> str:
    method_metrics_result = dict()
    if comparation_metrics != None:
      comparation_metrics_count = len(comparation_metrics)
    else:
      comparation_metrics = []
      comparation_metrics_count = self.comparation_metrics_containter.get_metrics_count()
    if ComparationMetricEnum.compression_rate.value not in comparation_metrics:
      comparation_metrics.append(ComparationMetricEnum.compression_rate)

    for name, compressor in self.compressors.items():
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      result = self.comparation_metrics_containter.compute_metrics(data, compressed_data, comparation_metrics)
      result[ComparationMetricEnum.compression_rate.value] *= 1 + comparation_metrics_count * 0.2
      method_metrics_result[name] = result

    agregated_metrics = dict()
    for method_name, metrics_value in method_metrics_result.items():
      agregated_metrics[method_name] = sum(metrics_value.values())
    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: -item[1])
    best_method_name, _ = sorted_methods[0]
    return best_method_name

  def get_best_with_weights_strategy(self, data: List[Measurement], weights: Dict[ComparationMetricEnum, float]) -> str:
    method_metrics_result = dict()
    comparation_metrics = list(weights.keys())

    for name, compressor in self.compressors.items():
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      result = self.comparation_metrics_containter.compute_metrics(data, compressed_data, comparation_metrics)
      for metric_name, weight in weights.items():
        result[metric_name.value] *= weight
      method_metrics_result[name] = result
    
    agregated_metrics = dict()
    for method_name, metrics_value in method_metrics_result.items():
      agregated_metrics[method_name] = sum(metrics_value.values())
    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: -item[1])
    best_method_name, _ = sorted_methods[0]
    return best_method_name

  def get_best_with_constraint_strategy(self, data: List[Measurement], constraints: Dict[ComparationMetricEnum, float]) -> str:
    method_metrics_result = dict()
    comparation_metrics = list(constraints.keys())
    if ComparationMetricEnum.compression_rate not in comparation_metrics:
      comparation_metrics.append(ComparationMetricEnum.compression_rate)

    for name, compressor in self.compressors.items():
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      result = self.comparation_metrics_containter.compute_metrics(data, compressed_data, comparation_metrics)
      pass_limits = True
      for metrics_name, constraint in constraints.items():
        if result[metrics_name.value] < constraint:
          pass_limits = False
          break
      if pass_limits:
        method_metrics_result[name] = result

    if len(method_metrics_result) == 0:
      return 'NoCompress'
        
    agregated_metrics = dict()
    for method_name, metrics_value in method_metrics_result.items():
      agregated_metrics[method_name] = metrics_value[ComparationMetricEnum.compression_rate.value], sum(metrics_value.values())

    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: (-item[1][0], -item[1][1]))
    best_method_name, _ = sorted_methods[0]
    return best_method_name
