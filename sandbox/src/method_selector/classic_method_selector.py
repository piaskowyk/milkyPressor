from src.metrics import Metric
from src.line_metrics import LineMetric
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
from src.data_compressor.compressor import Compressor
from typing import List, Dict
from collections import defaultdict as dict

class ClassicMethodSelector:

  def __init__(self) -> None:
    self.metrics_containter = Metric()
    self.line_metrics_container = LineMetric()
    self.compressors: Dict[str, Compressor] = {
      'CompressNTHS': CompressNTHS(),
      'CompressMinMax': CompressMinMax(),
      'CompressPWP': CompressPWP(),
      'CompressPIP_ED': CompressPIP_ED(),
      'CompressPIP_PD': CompressPIP_PD(),
      'CompressPIP_VD': CompressPIP_VD(),
      'CompressPAA': CompressPAA(),
      'CompressPAAVI': CompressPAAVI(),
      'CompressByChunk': CompressByChunk(),
      'CompressAPCADFT': CompressAPCADFT(),
      'CompressAPCAFFT': CompressAPCAFFT(),
      'CompressSTC': CompressSTC(),
      'CompressHigherDeriveration': CompressHigherDeriveration(),
    }

  def set_metrics(self):
    pass # todo

  def print_result(self, metric_result):
    for key, metrics in metric_result.items():
      print(key)
      for name, value in metrics.items():
        print(f"\t{name}:\t{value}")
  
  def safe_division(self, a, b):
    if b == 0:
      return 0
    else:
      return a / b

  def metrics_to_input(self, metrics):
    inputs = []
    for _, value in metrics.items():
      inputs.append(value)
    return inputs

  def get_best(self, data: List[Measurement]):
    metric_result = dict()
    for name, compressor in self.compressors.items():
      compressor.set_data(data)
      compressor.compress()
      compressed_data = compressor.compressed_data
      metric_result[name] = {
        'compression_rate': self.metrics_containter.compression_ratio_score(data, compressed_data) * 2,
        'sum_differences': self.metrics_containter.sum_differences_score(data, compressed_data),
        'arithmetic_average': self.metrics_containter.arithmetic_average_score(data, compressed_data),
        'standard_derivative': self.metrics_containter.standard_derivative_score(data, compressed_data),
        'function_field': self.metrics_containter.function_field_score(data, compressed_data),
        'diff_of_min': self.metrics_containter.diff_of_min_score(data, compressed_data),
        'diff_of_max': self.metrics_containter.diff_of_max_score(data, compressed_data),
        'min_max_diff': self.metrics_containter.min_max_diff_score(data, compressed_data),
        'value_crossing': self.metrics_containter.value_crossing_score(data, compressed_data),
        'positive_value_crossing': self.metrics_containter.positive_value_crossing_score(data, compressed_data),
        'negative_value_crossing': self.metrics_containter.negative_value_crossing_score(data, compressed_data),
        'peak_count': self.metrics_containter.peak_count_score(data, compressed_data),
        'positive_peak_count': self.metrics_containter.positive_peak_count_score(data, compressed_data),
        'negative_peak_count': self.metrics_containter.negative_peak_count_score(data, compressed_data),
        'median': self.metrics_containter.median_score(data, compressed_data),
        'covariance': self.metrics_containter.covariance_score(data, compressed_data),
        'corelation_pearson': self.metrics_containter.corelation_pearson_score(data, compressed_data),
        'corelation_spearman': self.metrics_containter.corelation_spearman_score(data, compressed_data),
      }
      # self.print_result(metric_result)
    agregated_metrics = dict()
    for method_name, metrics_value in metric_result.items():
      agregated_metrics[method_name] = sum(metrics_value.values())
    sorted_methods = sorted(agregated_metrics.items(), key=lambda item: -item[1])
    best_method_name = sorted_methods[0][0]
    return best_method_name, metric_result[best_method_name]
