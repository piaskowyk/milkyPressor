from typing import List
from fogml.generators import GeneratorFactory

from .data_type import Measurement
from .method_selector import MlMethodSelector

class ModelGenerator:
  def __init__(self) -> None:
    self.ml_method_selector: MlMethodSelector = MlMethodSelector()

  def set_measurements(self, measurements: List[Measurement] = None):
    self.ml_method_selector.set_measurements(measurements)

  def set_metrics(self):
    pass # todo

  def build(self):
    classifier, score = self.ml_method_selector.train()
    factory = GeneratorFactory()
    generator = factory.get_generator(classifier)
    generator.generate(fname='output.c')
    return score
