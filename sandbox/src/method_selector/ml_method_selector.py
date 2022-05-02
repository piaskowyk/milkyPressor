from typing import List
from sklearn import tree

from ..data_type import Measurement
from ..metric import SingleMetric, ComparationMetricEnum, SingleMetricEnum
from ..method_selector import ClassicMethodSelector
from ..measurement_provider import MeasurementProvider

class MlMethodSelector:
  def __init__(self) -> None:
    self.measurement_provider: MeasurementProvider = MeasurementProvider()
    self.measurements_set: List[List[Measurement]] = []
    self.single_metrics_container = SingleMetric()
    self.single_metrics = []
    self.comparation_metrics = []

  def set_measurements(self, measurements: List[List[Measurement]] = None):
    if measurements == None:
      self.measurements_set = self.measurement_provider.get_random1()
    else:
      self.measurements_set = measurements

  def set_metrics(self, single_metrics: List[SingleMetricEnum], comparation_metrics: List[ComparationMetricEnum]):
    self.single_metrics = single_metrics
    self.comparation_metrics = comparation_metrics

  def train(self):
    dataset = self._prepare_dataset()
    X_train = [data for data, _ in dataset]
    y_train = [label for _, label in dataset]
    X_test = [data for data, _ in dataset[:2]]
    y_test = [label for _, label in dataset[:2]]
    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    return classifier, score

  def _prepare_dataset(self):
    dataset = []
    for measurements in self.measurements_set:
      classic_method_selector = ClassicMethodSelector()
      classic_method_selector.set_metrics(self.comparation_metrics)
      best_method_name = classic_method_selector.get_best(measurements)
      single_metrics = self.single_metrics_container.compute_metrics(measurements, self.single_metrics)
      input = list(single_metrics.values())
      dataset.append([input, best_method_name])
    return dataset
