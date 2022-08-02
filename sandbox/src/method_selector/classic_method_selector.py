from src.data_compressor.compressors_provider import CompressorsProvider
from ..metric import SimilarityMetricEnum
from src.metric import SimilarityMetric
from src.data_type import Measurement
from src.data_compressor.compressor import Compressor
from typing import List, Dict, Callable, Tuple
from collections import defaultdict as dict

class ClassicMethodSelector:

  def __init__(self) -> None:
    self.comparation_metrics_containter = SimilarityMetric()
    self.similarity_metrics_container = SimilarityMetric()
    self.metrics = None

  def print_result(self, metric_result) -> None:
    for key, metrics in metric_result.items():
      print(key)
      for name, value in metrics.items():
        print(f"\t{name}:\t{value}")

  def compress_with_best_default_strategy(
      self, 
      data: List[Measurement], 
      comparation_metrics: List[SimilarityMetricEnum] = None,
      custom_metrics: List[Callable[[List[Measurement], List[Measurement]], float]] = []
    ) -> List[Measurement]:
    best_method_name, metrics_score = self.get_best_with_default_strategy(data, comparation_metrics, custom_metrics)
    compressor: Compressor = CompressorsProvider.get(best_method_name)
    compressor.set_data(data)
    compressor.compress()
    # compressor.vizualize()
    compression_metrics = self.similarity_metrics_container.compute_all(data, compressor.compressed_data)
    stats = compressor.get_stats()
    stats['method_name'] = best_method_name

    comparation_metrics_count = 0
    if comparation_metrics != None:
      comparation_metrics_count = len(comparation_metrics)
    else:
      comparation_metrics_count = self.comparation_metrics_containter.get_metrics_count()
    comparation_metrics_count += len(custom_metrics if custom_metrics != None else [])
    max_score = comparation_metrics_count + comparation_metrics_count * 0.2
    return compressor.compressed_data, stats, list(compression_metrics.values()), round(metrics_score / max_score * 100, 4)

  def get_best_with_default_strategy(
      self, 
      data: List[Measurement], 
      comparation_metrics: List[SimilarityMetricEnum] = None,
      custom_metrics: List[Callable[[List[Measurement], List[Measurement]], float]] = []
    ) -> Tuple[str, float]:
    method_metrics_result = dict()
    if comparation_metrics != None:
      comparation_metrics_count = len(comparation_metrics)
    else:
      comparation_metrics = self.comparation_metrics_containter.get_all_metric_list()
      comparation_metrics_count = self.comparation_metrics_containter.get_metrics_count()
    if SimilarityMetricEnum.compression_rate.value not in comparation_metrics:
      comparation_metrics.append(SimilarityMetricEnum.compression_rate)

    for name, compressor in CompressorsProvider.get_compressors().items():
      data = data[:]
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      if len(data) < len(compressed_data):
        print(len(data), len(compressed_data), name, compressor)
      result = self.comparation_metrics_containter.compute_metrics(data, compressed_data, comparation_metrics)
      for index, custom_metric in enumerate(custom_metrics):
        result[f'custom_{index}'] = custom_metric(data, compressed_data)
      result[SimilarityMetricEnum.compression_rate.value] *= 1 + comparation_metrics_count * 0.2
      method_metrics_result[name] = result
    agregated_metrics = dict()
    for method_name, metrics_value in method_metrics_result.items():
      agregated_metrics[method_name] = sum(metrics_value.values())
    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: -item[1])
    best_method_name, score = sorted_methods[0]
    return best_method_name, score

  def compress_with_best_weights_strategy(
      self, 
      data: List[Measurement], 
      weights: Dict[SimilarityMetricEnum, float],
      custom_metrics: List[Tuple[Callable[[List[Measurement], List[Measurement]], float], float]] = []
    ) -> List[Measurement]:
    best_method_name, metrics_score = self.get_best_with_weights_strategy(data, weights, custom_metrics)
    compressor: Compressor = CompressorsProvider.get(best_method_name)
    compressor.set_data(data)
    compressor.compress()
    # compressor.vizualize()
    compression_metrics = self.similarity_metrics_container.compute_all(data, compressor.compressed_data)
    stats = compressor.get_stats()
    stats['method_name'] = best_method_name
    max_score = sum(weights.values())
    for item, weight in custom_metrics:
      max_score += weight
    return compressor.compressed_data, stats, list(compression_metrics.values()), round(metrics_score / max_score * 100, 4)

  def get_best_with_weights_strategy(
      self, 
      data: List[Measurement], 
      weights: Dict[SimilarityMetricEnum, float],
      custom_metrics: List[Tuple[Callable[[List[Measurement], List[Measurement]], float], float]]
    ) -> str:
    method_metrics_result = dict()
    comparation_metrics = list(weights.keys())

    for name, compressor in CompressorsProvider.get_compressors().items():
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      result = self.comparation_metrics_containter.compute_metrics(data, compressed_data, comparation_metrics)
      for metric_name, weight in weights.items():
        result[metric_name.value] *= weight
      for index, custom_metric_with_weight in enumerate(custom_metrics):
        custom_metric, weight = custom_metric_with_weight
        result[f'custom_{index}'] = custom_metric(data, compressed_data) * weight
      method_metrics_result[name] = result
    
    agregated_metrics = dict()
    for method_name, metrics_value in method_metrics_result.items():
      agregated_metrics[method_name] = sum(metrics_value.values())
    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: -item[1])
    best_method_name, score = sorted_methods[0]
    return best_method_name, score

  def compress_with_best_constraint_strategy(
      self, 
      data: List[Measurement], 
      constraints: Dict[SimilarityMetricEnum, float],
      custom_metrics: List[Tuple[Callable[[List[Measurement], List[Measurement]], float], float]] = []
    ):
    best_method_name, metrics_score = self.get_best_with_constraint_strategy(data, constraints, custom_metrics)
    compressor: Compressor = CompressorsProvider.get(best_method_name)
    compressor.set_data(data)
    compressor.compress()
    # compressor.vizualize()
    compression_metrics = self.similarity_metrics_container.compute_all(data, compressor.compressed_data)
    stats = compressor.get_stats()
    stats['method_name'] = best_method_name
    max_score = len(constraints.values()) + len(custom_metrics)
    return compressor.compressed_data, stats, list(compression_metrics.values()), round(metrics_score / max_score * 100, 4)

  def get_best_with_constraint_strategy(
      self, 
      data: List[Measurement], 
      constraints: Dict[SimilarityMetricEnum, float],
      custom_metrics: List[Tuple[Callable[[List[Measurement], List[Measurement]], float], float]]
    ) -> str:
    method_metrics_result = dict()
    comparation_metrics = list(constraints.keys())
    if SimilarityMetricEnum.compression_rate not in comparation_metrics:
      comparation_metrics.append(SimilarityMetricEnum.compression_rate)

    max_result = self.comparation_metrics_containter.compute_metrics(data, data, comparation_metrics)
    for name, compressor in CompressorsProvider.get_compressors().items():
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      result = self.comparation_metrics_containter.compute_metrics(data, compressed_data, comparation_metrics)
      pass_limits = True
      for metrics_name, constraint in constraints.items():
        if result[metrics_name.value] < constraint:
          pass_limits = False
          break
      for index, custom_metric_with_constraint in enumerate(custom_metrics):
        custom_metric, constraint = custom_metric_with_constraint
        metric_value = custom_metric(data, compressed_data)
        result[f'custom_{index}'] = metric_value
        if metric_value < constraint:
          pass_limits = False
          break
      if pass_limits:
        method_metrics_result[name] = result

    if len(method_metrics_result) == 0:
      return 'NoCompress', sum(max_result.values())
        
    agregated_metrics = dict()
    for method_name, metrics_value in method_metrics_result.items():
      agregated_metrics[method_name] = metrics_value[SimilarityMetricEnum.compression_rate.value], sum(metrics_value.values())

    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: (-item[1][0], -item[1][1]))
    best_method_name, score = sorted_methods[0]
    return best_method_name, score[1]

  def compute_similarity_with_default_strategy(
      self,
      original_data: List[Measurement], 
      compressed_data: List[Measurement], 
      comparation_metrics: List[SimilarityMetricEnum] = None,
      custom_metrics: List[Callable[[List[Measurement], List[Measurement]], float]] = []
    ) -> float:
    if comparation_metrics != None:
      comparation_metrics_count = len(comparation_metrics)
    else:
      comparation_metrics = self.comparation_metrics_containter.get_all_metric_list()
      comparation_metrics_count = self.comparation_metrics_containter.get_metrics_count()
    if SimilarityMetricEnum.compression_rate.value not in comparation_metrics:
      comparation_metrics.append(SimilarityMetricEnum.compression_rate)

    result = self.comparation_metrics_containter.compute_metrics(original_data, compressed_data, comparation_metrics)
    for index, custom_metric in enumerate(custom_metrics):
      result[f'custom_{index}'] = custom_metric(original_data, compressed_data)
    result[SimilarityMetricEnum.compression_rate.value] *= 1 + comparation_metrics_count * 0.2
    score = sum(result.values())
    max_score = comparation_metrics_count + comparation_metrics_count * 0.2
    return round(score / max_score * 100, 4)

  def compute_similarity_with_weights_strategy(
      self,
      original_data: List[Measurement], 
      compressed_data: List[Measurement],
      weights: Dict[SimilarityMetricEnum, float],
      custom_metrics: List[Tuple[Callable[[List[Measurement], List[Measurement]], float], float]] = []
    ) -> float:
    comparation_metrics = list(weights.keys())
    result = self.comparation_metrics_containter.compute_metrics(original_data, compressed_data, comparation_metrics)
    max_score = 0
    for metric_name, weight in weights.items():
      result[metric_name.value] *= weight
      max_score += weight
    for index, custom_metric_with_weight in enumerate(custom_metrics):
      custom_metric, weight = custom_metric_with_weight
      result[f'custom_{index}'] = custom_metric(original_data, compressed_data) * weight
      max_score += weight
    score = sum(result.values())
    return round(score / max_score * 100, 4)

  def compute_similarity_with_constraint_strategy(
      self,
      original_data: List[Measurement], 
      compressed_data: List[Measurement],
      constraints: Dict[SimilarityMetricEnum, float],
      custom_metrics: List[Tuple[Callable[[List[Measurement], List[Measurement]], float], float]] = []
    ) -> float:
    comparation_metrics = list(constraints.keys())
    if SimilarityMetricEnum.compression_rate not in comparation_metrics:
      comparation_metrics.append(SimilarityMetricEnum.compression_rate)

    result = self.comparation_metrics_containter.compute_metrics(original_data, compressed_data, comparation_metrics)
    pass_limits = True
    for metrics_name, constraint in constraints.items():
      if result[metrics_name.value] < constraint:
        pass_limits = False
        break
    for index, custom_metric_with_constraint in enumerate(custom_metrics):
      custom_metric, constraint = custom_metric_with_constraint
      metric_value = custom_metric(original_data, compressed_data)
      result[f'custom_{index}'] = metric_value
      if metric_value < constraint:
        pass_limits = False
        break
    
    if len(original_data) == len(compressed_data):
      pass_limits = True

    if comparation_metrics != None:
      comparation_metrics_count = len(comparation_metrics)
    else:
      comparation_metrics_count = self.comparation_metrics_containter.get_metrics_count()
    comparation_metrics_count += len(custom_metrics)
    score = sum(result.values())
    max_score = comparation_metrics_count

    return round(score / max_score * 100, 4) if pass_limits else 100
