from src.model_generator import ModelGenerator
from src.metric import FeatureMetricEnum, ComparationMetricEnum

model_generator = ModelGenerator()
model_generator.set_measurements()
model_generator.set_single_metrics([
  FeatureMetricEnum.arithmetic_average,
  FeatureMetricEnum.median,
  FeatureMetricEnum.min_max_diff,
])
model_generator.add_custom_feature_metric(lambda data: 0.5)

model_generator.use_default_strategy([
  ComparationMetricEnum.arithmetic_average,
  ComparationMetricEnum.median,
  ComparationMetricEnum.min_max_diff,
])
# model_generator.add_custom_comparation_metric(lambda original, compressed: 0.5)

# model_generator.use_weights_strategy({
#   ComparationMetricEnum.compression_rate: 5,
#   ComparationMetricEnum.arithmetic_average: 2,
#   ComparationMetricEnum.median: 3,
#   ComparationMetricEnum.min_max_diff: 1.5,
# })
# model_generator.add_custom_comparation_metric_with_weight(lambda original, compressed: 0.5, 1)

# model_generator.use_constraint_strategy({
#   ComparationMetricEnum.compression_rate: 5,
#   ComparationMetricEnum.arithmetic_average: 2,
#   ComparationMetricEnum.median: 3,
#   ComparationMetricEnum.min_max_diff: 1.5,
# })
# model_generator.add_custom_comparation_metric_with_constraint(lambda original, compressed: 0.5, 0.6)

score = model_generator.build()
print(f'score: {score}')
