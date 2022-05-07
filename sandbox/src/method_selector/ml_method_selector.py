from typing import Dict, List
from enum import Enum
from sklearn import tree
from src.data_compressor.compressor import Compressor
from src.data_compressor.compressors_provider import CompressorsProvider

from ..data_type import Measurement
from ..metric import FeatureMetric, ComparationMetricEnum, FeatureMetricEnum
from ..method_selector import ClassicMethodSelector
from ..measurement_provider import MeasurementProvider

class StrategyEnum(Enum):
  DEFAULT = 1
  WEIGHTS = 2
  CONSTRAINTS = 3

class MlMethodSelector:
  def __init__(self) -> None:
    self.measurement_provider: MeasurementProvider = MeasurementProvider()
    self.measurements_set: List[List[Measurement]] = []
    self.feature_metrics_container = FeatureMetric()
    self.single_metrics: List[FeatureMetricEnum] = None
    self.comparation_metrics: List[ComparationMetricEnum] = None
    self.classifier = None
    self.weights: Dict[ComparationMetricEnum, float] = dict()
    self.constraints: Dict[ComparationMetricEnum, float] = dict()
    self.strategy: StrategyEnum = StrategyEnum.DEFAULT

  def set_measurements(self, measurements: List[List[Measurement]] = None):
    if measurements == None:
      self.measurements_set = self.measurement_provider.get_random1()
    else:
      self.measurements_set = measurements

  def set_single_metrics(self, single_metrics: List[FeatureMetricEnum]):
    self.single_metrics = single_metrics

  def use_default_strategy(self, comparation_metrics: List[ComparationMetricEnum]):
    self.strategy = StrategyEnum.DEFAULT
    self.comparation_metrics = comparation_metrics

  def use_weights_strategy(self, weights: Dict[ComparationMetricEnum, float]):
    self.strategy = StrategyEnum.WEIGHTS
    self.comparation_metrics = list(weights.keys())
    self.weights = weights

  def use_constraint_strategy(self, constraints: Dict[ComparationMetricEnum, float]):
    self.strategy = StrategyEnum.CONSTRAINTS
    self.comparation_metrics = list(constraints.keys())
    self.constraints = constraints

  def train(self):
    dataset = self._prepare_dataset()
    X_train = [data for data, _ in dataset]
    y_train = [label for _, label in dataset]
    X_test = [data for data, _ in dataset[:2]]
    y_test = [label for _, label in dataset[:2]]
    classifier = tree.DecisionTreeClassifier()
    self.classifier = classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    return score

  def get_classifier(self):
    return self.classifier

  def compress_with_best(self, data: List[Measurement]) -> List[Measurement]:
    single_metrics = self.feature_metrics_container.compute_metrics(data, self.single_metrics)
    input = list(single_metrics.values())
    best_method_name = self.classifier.predict([input])[0]
    compressor: Compressor = CompressorsProvider.get(best_method_name)
    compressor.set_data(data)
    compressor.compress()
    stats = compressor.get_stats()
    stats['method_name'] = best_method_name
    return compressor.compressed_data, stats

  def _prepare_dataset(self):
    dataset = []
    for measurements in self.measurements_set:
      classic_method_selector = ClassicMethodSelector()

      if self.strategy == StrategyEnum.DEFAULT:
        best_method_name = classic_method_selector.get_best_with_default_strategy(measurements, self.comparation_metrics)
      elif self.strategy == StrategyEnum.WEIGHTS:
        best_method_name = classic_method_selector.get_best_with_weights_strategy(measurements, self.weights)
      else:
        best_method_name = classic_method_selector.get_best_with_constraint_strategy(measurements, self.constraints)

      single_metrics = self.feature_metrics_container.compute_metrics(measurements, self.single_metrics)
      input = list(single_metrics.values())
      dataset.append([input, best_method_name])
    return dataset

  def add_custom_feature_metric(self, metric_function):
    pass

  def add_custom_comparation_metric(self, metric_function):
    pass

  def add_custom_comparation_metric_with_weight(self, metric_function, weight: float):
    pass

  def add_custom_comparation_metric_with_constraint(self, metric_function, constraint: float):
    pass
