from calendar import c
import math
from re import S
import matplotlib.pyplot as plt
from typing import Tuple, Any, List
import numpy as np
import statistics
from src.data_type import Measurement

class ComparationMetric:

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
  
  def _cacl_score(self, original_value: float, transformed_value: float) -> float:
    if original_value == 0:
      return 1
    score = 1 - abs((original_value - transformed_value) / original_value)
    # if score > 1 or score < 0:
    #   raise Exception(f"score problem: {score}, {original_value}, {transformed_value}")
    return max(0, score)

  def sum_differences_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original_data_count = len(original)
    if original_data_count < 2:
      return 1
    transformed = self._interpolate_data(original, transformed)
    transformed_diff = sum([math.fabs(original[i].value - transformed[i].value) for i in range(len(original))])
    point_a = original[0]
    point_b = original[original_data_count - 1]
    f_a = (point_b.value - point_a.value) / (point_b.timestamp - point_a.timestamp)
    f_b = (point_b.timestamp * point_a.value - point_a.timestamp * point_b.value) / (point_b.timestamp - point_a.timestamp)
    maximum_diff = sum([math.fabs(original[i].value - (f_a * original[i].timestamp + f_b)) for i in range(len(original))])
    score = 1 - transformed_diff / maximum_diff
    return max(score, 0)
  
  def arithmetic_average_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original = self._strip_data(original)
    transformed = self._strip_data(transformed)
    original_avg = sum(original) / len(original)
    transformed_avg = sum(transformed) / len(transformed)
    return self._cacl_score(original_avg, transformed_avg)

  def standard_derivative_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original = self._strip_data(original)
    original_mean = self._mean(original)
    n = len(original)
    original_standard_derivative = math.sqrt(sum([(original[i] - original_mean)**2 for i in range(n)]) / n)
    transformed = self._strip_data(transformed)
    transformed_mean = self._mean(transformed)
    n = len(transformed)
    transformed_standard_derivative = math.sqrt(sum([(transformed[i] - transformed_mean)**2 for i in range(n)]) / n)
    return self._cacl_score(original_standard_derivative, transformed_standard_derivative)
    
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

  def function_field_score(self, original: List[Measurement], transformed: List[float]) -> float:
    original_field = self._function_field(original)
    transformed_field = self._function_field(transformed)
    return self._cacl_score(original_field, transformed_field)

  def diff_of_min_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original_min = min(self._strip_data(original))
    trnsformed_min = min(self._strip_data(transformed))
    return self._cacl_score(original_min, trnsformed_min)

  def diff_of_max_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original_max = max(self._strip_data(original))
    trnsformed_max = max(self._strip_data(transformed))
    return self._cacl_score(original_max, trnsformed_max)

  def min_max_diff_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    transformed = self._strip_data(transformed)
    transformed_diff = abs(max(transformed) - min(transformed))
    original = self._strip_data(original)
    original_diff = abs(max(original) - min(original))
    return self._cacl_score(original_diff, transformed_diff)

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

  def value_crossing_score(
      self, 
      original: List[Measurement], 
      transformed: List[Measurement],
      direction: int = 0
    ) -> float:
    original = self._strip_data(original)
    transformed = self._strip_data(transformed)
    border = self._mean(original)
    threshold = border * 0.01
    original_cross_count = self._value_crossing(original, border, threshold, direction)
    transformed_cross_count = self._value_crossing(transformed, border, threshold, direction)
    if original_cross_count == 0:
      original_cross_count = 1
    return self._cacl_score(original_cross_count, transformed_cross_count)

  def positive_value_crossing_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    return self.value_crossing_score(original, transformed, 1)

  def negative_value_crossing_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    return self.value_crossing_score(original, transformed, -1)

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

  def peak_count_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original_peaks_count = self._get_peaks_count(original, 0)
    transformed_peaks_count = self._get_peaks_count(transformed, 0)
    return self._cacl_score(original_peaks_count, transformed_peaks_count)

  def positive_peak_count_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original_peaks_count = self._get_peaks_count(original, 1)
    transformed_peaks_count = self._get_peaks_count(transformed, 1)
    return self._cacl_score(original_peaks_count, transformed_peaks_count)

  def negative_peak_count_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original_peaks_count = self._get_peaks_count(original, -1)
    transformed_peaks_count = self._get_peaks_count(transformed, -1)
    return self._cacl_score(original_peaks_count, transformed_peaks_count)

  def median_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    original_median = statistics.median(self._strip_data(original))
    transformed_median = statistics.median(self._strip_data(transformed))
    return self._cacl_score(original_median, transformed_median)
  
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

  def covariance_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    x_list = [i for i in range(len(transformed))]
    original_covariance = self._covariance(x_list, self._strip_data(original))
    transformed_covariance = self._covariance(x_list, self._strip_data(transformed))
    return self._cacl_score(original_covariance, transformed_covariance)

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

  def corelation_pearson_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    x_list = [i for i in range(len(transformed))]
    original_corelation = self._corelation_pearson(x_list, self._strip_data(original))
    transformed_corelation = self._corelation_pearson(x_list, self._strip_data(transformed))
    return self._cacl_score(original_corelation, transformed_corelation)

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

  def corelation_spearman_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    x_list = [i for i in range(len(transformed))]
    original_corelation = self._corelation_spearman_on_injection(x_list, self._strip_data(original))
    transformed_corelation = self._corelation_spearman_on_injection(x_list, self._strip_data(transformed))
    return self._cacl_score(original_corelation, transformed_corelation)

  def compression_ratio_score(self, original: List[Measurement], transformed: List[Measurement]) -> float:
    return 1 - len(transformed) / len(original)