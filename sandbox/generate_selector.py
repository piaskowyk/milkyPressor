from src.model_generator import ModelGenerator
from src.metric import SingleMetricEnum, ComparationMetricEnum

model_generator = ModelGenerator()
model_generator.set_measurements()
model_generator.set_single_metrics([
  SingleMetricEnum.arithmetic_average,
  SingleMetricEnum.median,
  SingleMetricEnum.min_max_diff,
])
model_generator.set_default_strategy([
  ComparationMetricEnum.arithmetic_average,
  ComparationMetricEnum.median,
  ComparationMetricEnum.min_max_diff,
])
# model_generator.use_weights_strategy({
#   ComparationMetricEnum.compression_rate: 5,
#   ComparationMetricEnum.arithmetic_average: 2,
#   ComparationMetricEnum.median: 3,
#   ComparationMetricEnum.min_max_diff: 1.5,
# })
# model_generator.use_constraint_strategy({
#   ComparationMetricEnum.compression_rate: 5,
#   ComparationMetricEnum.arithmetic_average: 2,
#   ComparationMetricEnum.median: 3,
#   ComparationMetricEnum.min_max_diff: 1.5,
# })
score = model_generator.build()
print(f'score: {score}')
