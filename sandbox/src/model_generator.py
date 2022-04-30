# todo:
# - wygeneruj model
# - wybierz metryki

from signal_generator import SignalGenerator
from metrics import Metric
from data_type import Measurement
import matplotlib.pyplot as plt
from data_compressor.other import CompressNTHS
from data_compressor.other import CompressMinMax
from data_compressor.other import CompressPWP
from data_compressor.pip import CompressPIP_ED
from data_compressor.pip import CompressPIP_PD
from data_compressor.pip import CompressPIP_VD
from data_compressor.paa import CompressPAA
from data_compressor.paa import CompressPAAVI
from data_compressor.paa import CompressByChunk
from data_compressor.pla import CompressAPCADFT
from data_compressor.pla import CompressAPCAFFT
from data_compressor.pla import CompressSTC
from data_compressor.pla import CompressHigherDeriveration
from data_type import Measurement
from data_compressor.compressor import Compressor
from typing import List, Dict
from collections import defaultdict as dict
from method_selector import ClassicMethodSelector, MlMethodSelector
from measurement_provider import MeasurementProvider

from sklearn import tree
from fogml.generators import GeneratorFactory

class ModelGenerator:
  def __init__(self) -> None:
    self.measurement_provider: MeasurementProvider = MeasurementProvider()
    self.measurements_set: List[Measurement] = []
    self.ml_method_selector: ClassicMethodSelector = MlMethodSelector()

  def set_measurements(self, measurements: List[Measurement] = None):
    if measurements == None:
      self.measurements_set = self.measurement_provider.get_random1()
    else:
      self.measurements_set = measurements

  def build(self):
    dataset_size = len(dataset)

    X_train = [data for data, label in dataset]
    y_train = [label for data, label in dataset]

    X_test = [data for data, label in dataset[:2]]
    y_test = [label for data, label in dataset[:2]]

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    print(f'Score: {score}')

    factory = GeneratorFactory()
    generator = factory.get_generator(clf)
    generator.generate(fname='output.c')
  
  def _prepare_dataset(self):
    dataset = []
    for measurements in self.measurements_set:
      classic_method_selector = ClassicMethodSelector()
      best_method_name = AlgorythmSelector().get_best(measurements)[0].__class__.__name__
      algorythm_selector = AlgorythmSelector()
      input = algorythm_selector.metrics_to_input(algorythm_selector.compute_line_metrics_for_data(measurements))
      dataset.append([input, best_method_name])
    return dataset
