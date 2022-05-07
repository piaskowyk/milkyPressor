from typing import List, Dict
from fogml.generators import GeneratorFactory
from .metric import ComparationMetricEnum, FeatureMetricEnum
from .data_type import Measurement
from .method_selector import MlMethodSelector

class ModelGenerator:
  def __init__(self) -> None:
    self.ml_method_selector: MlMethodSelector = MlMethodSelector()

  def set_measurements(self, measurements: List[Measurement] = None) -> None:
    self.ml_method_selector.set_measurements(measurements)

  def set_single_metrics(self, single_metrics: List[FeatureMetricEnum]) -> None:
    self.ml_method_selector.set_single_metrics(single_metrics)

  def use_default_strategy(self, comparation_metrics: List[ComparationMetricEnum]) -> None:
    self.ml_method_selector.use_default_strategy(comparation_metrics)

  def use_weights_strategy(self, weights: Dict[ComparationMetricEnum, float]) -> None:
    self.ml_method_selector.use_weights_strategy(weights)

  def use_constraint_strategy(self, constraints: Dict[ComparationMetricEnum, float]) -> None:
    self.ml_method_selector.use_constraint_strategy(constraints)

  def build(self) -> float:
    score = self.ml_method_selector.train()
    classifier = self.ml_method_selector.get_classifier()
    factory = GeneratorFactory()
    generator = factory.get_generator(classifier)
    generator.generate(fname='output.c')
    return score

  def add_custom_feature_metric(self, metric_function) -> None:
    self.ml_method_selector.add_custom_feature_metric(metric_function)

  def add_custom_comparation_metric(self, metric_function) -> None:
    self.ml_method_selector.add_custom_comparation_metric(metric_function)

  def add_custom_comparation_metric_with_weight(self, metric_function) -> None:
    self.ml_method_selector.add_custom_comparation_metric_with_weight(metric_function)

  def add_custom_comparation_metric_with_constraint(self, metric_function) -> None:
    self.ml_method_selector.add_custom_comparation_metric_with_constraint(metric_function)
