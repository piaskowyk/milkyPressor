# todo:
# - wybierz metryki

from metric import SingleMetric
from data_type import Measurement
from typing import List
from method_selector import ClassicMethodSelector, MlMethodSelector
from measurement_provider import MeasurementProvider

from sklearn import tree
from fogml.generators import GeneratorFactory

class ModelGenerator:
  def __init__(self) -> None:
    self.measurement_provider: MeasurementProvider = MeasurementProvider()
    self.measurements_set: List[Measurement] = []
    self.ml_method_selector: ClassicMethodSelector = MlMethodSelector()
    self.single_metrics_container = SingleMetric()

  def set_measurements(self, measurements: List[Measurement] = None):
    if measurements == None:
      self.measurements_set = self.measurement_provider.get_random1()
    else:
      self.measurements_set = measurements

  def build(self):
    dataset = self._prepare_dataset()
    X_train = [data for data, _ in dataset]
    y_train = [label for _, label in dataset]

    X_test = [data for data, _ in dataset[:2]]
    y_test = [label for _, label in dataset[:2]]

    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(X_train, y_train)

    score = classifier.score(X_test, y_test)

    factory = GeneratorFactory()
    generator = factory.get_generator(classifier)
    generator.generate(fname='output.c')
    return score
  
  def _prepare_dataset(self):
    dataset = []
    for measurements in self.measurements_set:
      classic_method_selector = ClassicMethodSelector()
      best_method_name = classic_method_selector.get_best(measurements)
      input = self.single_metrics_container.compute_all(measurements)
      dataset.append([input, best_method_name])
    return dataset
