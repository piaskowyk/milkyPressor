from typing import Dict, List, Callable, Tuple
from enum import Enum
from src.metric.similarity_metrics import SimilarityMetric
from sklearn import tree
from src.data_compressor.compressor import Compressor
from src.data_compressor.compressors_provider import CompressorsProvider
import random

from ..data_type import Measurement
from ..metric import FeatureMetric, SimilarityMetricEnum, FeatureMetricEnum
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
    self.similarity_metrics_container = SimilarityMetric()
    self.single_metrics: List[FeatureMetricEnum] = None
    self.comparation_metrics: List[SimilarityMetricEnum] = None
    self.classifier = None
    self.weights: Dict[SimilarityMetricEnum, float] = dict()
    self.constraints: Dict[SimilarityMetricEnum, float] = dict()
    self.strategy: StrategyEnum = StrategyEnum.DEFAULT
    self.custom_feature_metric: List[Callable[[List[Measurement]], float]] = []
    self.custom_comparation_metric: List[Callable[[List[Measurement]], float]] = []
    self.custom_comparation_metric_with_weight: List[Tuple[Callable[[List[Measurement]], float], float]] = []
    self.custom_comparation_metric_with_constraint: List[Tuple[Callable[[List[Measurement]], float], float]] = []

  def set_measurements(self, measurements: List[List[Measurement]] = None):
    if measurements == None:
      self.measurements_set = self.measurement_provider.get_random1()
    else:
      self.measurements_set = measurements

  def set_single_metrics(self, single_metrics: List[FeatureMetricEnum]):
    self.single_metrics = single_metrics

  def use_default_strategy(self, comparation_metrics: List[SimilarityMetricEnum]):
    self.strategy = StrategyEnum.DEFAULT
    self.comparation_metrics = comparation_metrics

  def use_weights_strategy(self, weights: Dict[SimilarityMetricEnum, float]):
    self.strategy = StrategyEnum.WEIGHTS
    self.comparation_metrics = list(weights.keys())
    self.weights = weights

  def use_constraint_strategy(self, constraints: Dict[SimilarityMetricEnum, float]):
    self.strategy = StrategyEnum.CONSTRAINTS
    self.comparation_metrics = list(constraints.keys())
    self.constraints = constraints

  def split_dataset(self, dataset):
    dataset_pivot = int(len(dataset) * 0.8)
    train_dataset = dataset[:dataset_pivot]
    test_dataset = dataset[dataset_pivot:]
    X_train = [data for data, _ in train_dataset]
    y_train = [label for _, label in train_dataset]
    X_test = [data for data, _ in test_dataset]
    y_test = [label for _, label in test_dataset]
    return X_train, y_train, X_test, y_test

  def calc_custom_score(self, X_test, y_test):
    data_count = len(X_test)
    success_counter = 0
    for i in range(data_count):
      expected_label = y_test[i]
      predicted_label = self.classifier.predict([X_test[i]])[0]
      if expected_label.split('_')[0] == predicted_label.split('_')[0]:
        success_counter += 1
    return success_counter / data_count

  def train(self):
    dataset = self._prepare_dataset()
    X_train, y_train, X_test, y_test = self.split_dataset(dataset)
    classifier = tree.DecisionTreeClassifier()
    self.classifier = classifier.fit(X_train, y_train)
    # from matplotlib import pyplot as plt
    # plt.figure(figsize=(60,30))  # set plot size (denoted in inches)
    # tree.plot_tree(classifier, fontsize=10, class_names=True)
    # plt.show()
    score_1 = classifier.score(X_test, y_test)
    score_2 = self.calc_custom_score(X_test, y_test)
    return score_1, score_2

  def get_classifier(self):
    return self.classifier

  def compress_with_best(self, data: List[Measurement]) -> List[Measurement]:
    single_metrics = self.feature_metrics_container.compute_metrics(
      data, 
      self.single_metrics,
      self.custom_feature_metric
    )
    input = list(single_metrics.values())
    best_method_name = self.classifier.predict([input])[0]
    compressor: Compressor = CompressorsProvider.get(best_method_name)
    compressor.set_data(data)
    compressor.compress()
    compression_metrics = self.similarity_metrics_container.compute_all(data, compressor.compressed_data)
    stats = compressor.get_stats()
    # compressor.vizualize()
    stats['method_name'] = best_method_name
    return compressor.compressed_data, stats, list(compression_metrics.values())

  def _prepare_dataset(self):
    dataset = []
    random.shuffle(self.measurements_set)
    for measurements in self.measurements_set:
      classic_method_selector = ClassicMethodSelector()

      if self.strategy == StrategyEnum.DEFAULT:
        best_method_name, _ = classic_method_selector.get_best_with_default_strategy(
          measurements, 
          self.comparation_metrics,
          self.custom_comparation_metric
        )
      elif self.strategy == StrategyEnum.WEIGHTS:
        best_method_name, _ = classic_method_selector.get_best_with_weights_strategy(
          measurements, 
          self.weights,
          self.custom_comparation_metric_with_weight
        )
      else:
        best_method_name, _ = classic_method_selector.get_best_with_constraint_strategy(
          measurements, 
          self.constraints,
          self.custom_comparation_metric_with_constraint
        )

      single_metrics = self.feature_metrics_container.compute_metrics(
        measurements, 
        self.single_metrics,
        self.custom_feature_metric
      )
      input = list(single_metrics.values())
      dataset.append([input, best_method_name])
    return dataset

  def add_custom_feature_metric(self, metric_function: Callable[[List[Measurement]], float]) -> None:
    self.custom_feature_metric.append(metric_function)

  def add_custom_similarity_metric(self, metric_function: Callable[[List[Measurement]], float]) -> None:
    self.custom_comparation_metric.append(metric_function)

  def add_custom_similarity_metric_with_weight(self, metric_function: Callable[[List[Measurement]], float], weight: float) -> None:
    self.custom_comparation_metric_with_weight.append((metric_function, weight))

  def add_custom_similarity_metric_with_constraint(self, metric_function: Callable[[List[Measurement]], float], constraint: float) -> None:
    self.custom_comparation_metric_with_constraint.append((metric_function, constraint))
