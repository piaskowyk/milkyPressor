from enum import Enum
import math
import matplotlib.pyplot as plt
from typing import Tuple, Any, List
import numpy as np
import statistics
from src.data_type import Measurement

class SingleMetricEnum(Enum):
  arithmetic_average = 'arithmetic_average'
  standard_derivative = 'standard_derivative'
  function_field = 'function_field'
  min_value = 'min_value'
  max_value = 'max_value'
  min_max_diff = 'min_max_diff'
  value_crossing = 'value_crossing'
  positive_value_crossing = 'positive_value_crossing'
  negative_value_crossing = 'negative_value_crossing'
  peak_count = 'peak_count'
  positive_peak_count = 'positive_peak_count'
  negative_peak_count = 'negative_peak_count'
  median = 'median'
  covariance = 'covariance'
  corelation_pearson = 'corelation_pearson'
  corelation_spearman = 'corelation_spearman'
  
class SingleMetric:

  def _strip_data(self, data: List[Measurement]):
    return [item.value for item in data]

  def _interpolate_points(self, x: int, point_A: Measurement, point_B: Measurement) -> float:
    return ((point_B.value - point_A.value) / (point_B.timestamp - point_A.timestamp)) * x \
      + ((point_B.timestamp * point_A.value - point_A.timestamp * point_B.value) / (point_B.timestamp - point_A.timestamp))

  def _interpolate_data(self, original: List[Measurement], transformed: List[Measurement]) -> List[Measurement]:
    interpolated = []
    current_index = 0
    transformed_count = len(transformed)
    data_original_count = len(original)
    if data_original_count < 2:
      return original
    first = original[0]
    if first.timestamp != transformed[0].timestamp:
      transformed = [Measurement(first.value, first.timestamp)] + transformed

    data_transformed_count = len(transformed)
    last = original[data_original_count - 1]
    if last.timestamp != transformed[data_transformed_count - 1].timestamp:
      transformed.append(Measurement(last.value, last.timestamp))
    transformed_count = len(transformed)

    for original_measurement in original:
      for i in range(current_index, transformed_count):
        if transformed[i].timestamp == original_measurement.timestamp:
          interpolated.append(Measurement(original_measurement.value, original_measurement.timestamp))
          break
        elif transformed[i].timestamp > original_measurement.timestamp:
          current_index = i
          point_a = transformed[current_index - 1]
          point_b = transformed[current_index]
          x = original_measurement.timestamp
          y = self._interpolate_points(x, point_a, point_b)
          interpolated.append(Measurement(y, x))
          break
    return interpolated

  def _prepare_data(self, original: List[Measurement], transformed: List[Measurement]):
    return self._strip_data(self._interpolate_data(original, transformed))
  
  def data_count(self, data: List[Measurement]) -> float:
    return len(data)

  def sum_value(self, data: List[Measurement]) -> float:
    return sum(self._strip_data(data))

  def arithmetic_average(self, data: List[Measurement]) -> float:
    return sum(self._strip_data(data)) / len(data)

  def standard_derivative(self, data: List[Measurement]) -> float:
    data = self._strip_data(data)
    mean = self._mean(data)
    n = len(data)
    standard_derivative = math.sqrt(sum([(data[i] - mean)**2 for i in range(n)]) / n)
    return standard_derivative
    
  def _function_field(self, data: List[Measurement]) -> float:
    field = 0
    if len(data) < 2:
      return field
    for i in range(1, len(data)):
      h = data[i - 1].timestamp - data[i].timestamp
      a = data[i - 1].value
      b = data[i].value
      field += (a + b) * h / 2
    return field

  def function_field(self, data: List[Measurement]) -> float:
    field = self._function_field(data)
    return field

  def min_value(self, data: List[Measurement]) -> float:
    data_min = min(self._strip_data(data))
    return data_min

  def max_value(self, data: List[Measurement]) -> float:
    data_max = max(self._strip_data(data))
    return data_max

  def min_max_diff(self, data: List[Measurement]) -> float:
    diff = abs(self.max_value(data) - self.min_value(data))
    return diff

  def _value_crossing(self, data: List[float], border: float = 0, threshold: float = 0, direction: int = 0) -> float:
    if len(data) == 0:
      return 0

    counter = 0
    lastPosition = None
    position = None

    value = data[0]
    if value > border + threshold:
      lastPosition = 1
    elif value < border - threshold:
      lastPosition = -1
    else:
      lastPosition = 0
      counter = 1

    for value in data:
      if value > border + threshold:
        position = 1
      elif value < border - threshold:
        position = -1
      else:
        position = 0

      if direction == 0:
        if (position == 0 and lastPosition != 0) or (abs(position - lastPosition) == 2):
          counter += 1
      if direction > 0: # positive crossing
        if lastPosition < 0 and position != lastPosition:
          counter += 1
      if direction < 0: # negaive crossing
        if lastPosition > 0 and position != lastPosition:
          counter += 1

    return counter

  def value_crossing(
      self, 
      data: List[Measurement],
      direction: int = 0
    ) -> float:
    data = self._strip_data(data)
    border = self._mean(data)
    threshold = border * 0.01
    cross_count = self._value_crossing(data, border, threshold, direction)
    return cross_count

  def positive_value_crossing(self, data: List[Measurement]) -> float:
    return self.value_crossing(data, 1)

  def negative_value_crossing(self, data: List[Measurement]) -> float:
    return self.value_crossing(data, -1)

  def _peak_detector(
      self, 
      y: List[float], 
      x: List[int] = [], 
      delta: float = 0.3
    ) -> Tuple[Tuple[List[float], List[float]], Tuple[List[float], List[float]]]:
    maxtab = []
    mintab = [] 
    minimum = math.inf
    maximum = -math.inf
    minimum_x = None
    maximum_x = None
    look_for_max = True

    for i in range(len(y)):
        current = y[i]
        if current > maximum:
            maximum = current
            maximum_x = x[i]
        if current < minimum:
            minimum = current
            minimum_x = x[i]
        
        if look_for_max:
            if current < maximum - delta:
                maxtab.append((maximum_x, maximum))
                minimum = current
                minimum_x = x[i]
                look_for_max = False
        else:
            if current > minimum + delta:
                mintab.append((minimum_x, minimum))
                maximum = current
                maximum_x = x[i]
                look_for_max = True

    return [[i[0] for i in maxtab], [i[1] for i in maxtab]], [[i[0] for i in mintab], [i[1] for i in mintab]]

  def _get_peaks_count(self, data: List[Measurement], peak_type: int) -> float:
    data = self._strip_data(data)
    mean = self._mean(data)
    derive = max([min(data), max(data)])
    delta = abs(derive - mean) * 0.2
    peaks_positive, peaks_negative = self._peak_detector(data, [i for i in range(len(data))], delta)
    if peak_type < 0:
      return len(peaks_negative[0])
    elif peak_type == 0:
      return len(peaks_positive[0]) + len(peaks_negative[0])
    else:
      return len(peaks_positive[0])

  def peak_count(self, data: List[Measurement]) -> float:
    peaks_count = self._get_peaks_count(data, 0)
    return peaks_count

  def positive_peak_count(self, data: List[Measurement]) -> float:
    peaks_count = self._get_peaks_count(data, 1)
    return peaks_count

  def negative_peak_count(self, data: List[Measurement]) -> float:
    peaks_count = self._get_peaks_count(data, -1)
    return peaks_count

  def median(self, data: List[Measurement]) -> float:
    median = statistics.median(self._strip_data(data))
    return median
  
  def fft(self, transformed: List[float], show_plot: bool = False) -> Tuple[List[float], Any]:
    transformed_np_array = np.array(transformed)
    sp = np.fft.fft(transformed_np_array)
    freq = np.fft.fftfreq(transformed_np_array.shape[-1])
    if show_plot:
      plt.plot(freq, sp.real, freq, sp.imag)
    return sp, freq

  def _mean(self, data: List[float]) -> float:
    return sum(data) / len(data)

  def _covariance(self, x: List[float], y: List[float]) -> float:
    n = len(x)
    mean_x = self._mean(x)
    mean_y = self._mean(y)
    sum_distance = 0
    for i in range(n):
      sum_distance += (x[i] - mean_x) * (y[i] - mean_y)
    return sum_distance * 1/n

  def covariance(self, data: List[Measurement]) -> float:
    x_list = [i for i in range(len(data))]
    covariance = self._covariance(x_list, self._strip_data(data))
    return covariance

  def _corelation_pearson(self, x: List[float], y: List[float]) -> float:
    mean_x = self._mean(x)
    mean_y = self._mean(y)
    sum_distance = 0
    sum_distance_square_x = 0
    sum_distance_square_y = 0
    for i in range(len(x)):
      distance_x = (x[i] - mean_x)
      distance_y = (y[i] - mean_y)
      sum_distance += distance_x * distance_y
      sum_distance_square_x += distance_x ** 2
      sum_distance_square_y += distance_y ** 2
    distance_sqrt = math.sqrt(sum_distance_square_x * sum_distance_square_y)
    if distance_sqrt == 0:
      return 1
    return sum_distance / distance_sqrt

  def corelation_pearson(self, data: List[Measurement]) -> float:
    x_list = [i for i in range(len(data))]
    corelation = self._corelation_pearson(x_list, self._strip_data(data))
    return corelation

  def _corelation_spearman_on_injection(self, x: List[float], y: List[float]) -> float:
    data_len = len(x)
    n = data_len
    max_rang = data_len
    next_rang = max_rang
    x_rangs = [i + 1 for i in range(max_rang)]
    y_rangs = []
    i = 0
    while i < data_len:
      values_count = 1
      current_value = y[i]
      while i + values_count < data_len and y[i + values_count] == current_value:
        values_count += 1
      current_rang = sum(range(i, i + values_count)) / values_count
      for _ in range(values_count):
        y_rangs.append(current_rang)
      next_rang -= values_count
      i += values_count
    distance_sum = 0
    for i in range(data_len):
      distance_sum += (x_rangs[i] - y_rangs[i]) ** 2
    return 1 - ((6 * distance_sum) / (n * (n ** 2 - 1)))

  def corelation_spearman(self, data: List[Measurement]) -> float:
    x_list = [i for i in range(len(data))]
    corelation = self._corelation_spearman_on_injection(x_list, self._strip_data(data))
    return corelation

  def _print_result(self, metric_result):
    for key, metrics in metric_result.items():
      print(key)
      for name, value in metrics.items():
        print(f"\t{name}:\t{value}")

  def _safe_division(self, a, b):
    if b == 0:
      return 0
    else:
      return a / b

  def compute_all(self, data: List[Measurement]) -> List[float]:
    data_count = self.data_count(data)
    sum_value = self.sum_value(data)
    min_value = self.min_value(data)
    max_value = self.max_value(data)
    arithmetic_average = self.arithmetic_average(data)
    standard_derivative = self.standard_derivative(data)
    function_field = self.function_field(data)
    min_max_diff = self.min_max_diff(data)
    value_crossing = self.value_crossing(data)
    positive_value_crossing = self.positive_value_crossing(data)
    negative_value_crossing = self.negative_value_crossing(data)
    peak_count = self.peak_count(data)
    positive_peak_count = self.positive_peak_count(data)
    negative_peak_count = self.negative_peak_count(data)
    median = self.median(data)
    covariance = self.covariance(data)
    corelation_pearson = self.corelation_pearson(data)
    corelation_spearman = self.corelation_spearman(data)
    return {
      'arithmetic_average': self._safe_division(arithmetic_average, sum_value),
      'standard_derivative': standard_derivative,
      'function_field': self._safe_division(function_field, sum_value),
      'min_value': self._safe_division(min_value, max_value),
      'max_value': self._safe_division(max_value, min_value),
      'min_max_diff': self._safe_division(self._safe_division(min_max_diff, max_value), min_value),
      'value_crossing': self._safe_division(value_crossing, data_count),
      'positive_value_crossing': self._safe_division(positive_value_crossing, data_count),
      'negative_value_crossing': self._safe_division(negative_value_crossing, data_count),
      'peak_count': self._safe_division(peak_count, data_count),
      'positive_peak_count': self._safe_division(positive_peak_count, data_count),
      'negative_peak_count': self._safe_division(negative_peak_count, data_count),
      'median': self._safe_division(median, sum_value),
      'covariance': covariance,
      'corelation_pearson': corelation_pearson,
      'corelation_spearman': corelation_spearman,
    }

  def compute_metrics(self, data: List[Measurement], metrics: List[SingleMetricEnum] = None) -> List[float]:
    all_metrics = self.compute_all(data)
    if metrics == None:
      return all_metrics
    result = dict()
    for metric_name in metrics:
      result[metric_name.value] = all_metrics[metric_name.value]
    return result