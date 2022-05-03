from typing import List, Dict
from fogml.generators import GeneratorFactory
from .metric import ComparationMetricEnum, SingleMetricEnum
from .data_type import Measurement
from .method_selector import MlMethodSelector

class ModelGenerator:
  def __init__(self) -> None:
    self.ml_method_selector: MlMethodSelector = MlMethodSelector()

  def set_measurements(self, measurements: List[Measurement] = None):
    self.ml_method_selector.set_measurements(measurements)

  def set_single_metrics(self, single_metrics: List[SingleMetricEnum]):
    self.ml_method_selector.set_single_metrics(single_metrics)

  def set_default_strategy(self, comparation_metrics: List[ComparationMetricEnum]):
    self.ml_method_selector.set_default_strategy(comparation_metrics)

  def use_weights_strategy(self, weights: Dict[ComparationMetricEnum, float]):
    self.ml_method_selector.use_weights_strategy(weights)

  def use_constraint_strategy(self, constraints: Dict[ComparationMetricEnum, float]):
    self.ml_method_selector.use_constraint_strategy(constraints)

  def build(self):
    score = self.ml_method_selector.train()
    classifier = self.ml_method_selector.get_classifier()
    factory = GeneratorFactory()
    generator = factory.get_generator(classifier)
    generator.generate(fname='output.c')
    return score
