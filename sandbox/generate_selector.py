from src.model_generator import ModelGenerator
from src.metric import FeatureMetricEnum, SimilarityMetricEnum

model_generator = ModelGenerator()
model_generator.set_measurements()
model_generator.set_single_metrics([
  FeatureMetricEnum.arithmetic_average,
  FeatureMetricEnum.median,
  FeatureMetricEnum.min_max_diff,
])
model_generator.add_custom_feature_metric(lambda data: 0.5)

model_generator.use_default_strategy([
  SimilarityMetricEnum.arithmetic_average,
  SimilarityMetricEnum.median,
  SimilarityMetricEnum.min_max_diff,
])
model_generator.add_custom_similarity_metric(lambda original, compressed: 0.5)

# model_generator.use_weights_strategy({
#   SimilarityMetricEnum.compression_rate: 5,
#   SimilarityMetricEnum.arithmetic_average: 2,
#   SimilarityMetricEnum.median: 3,
#   SimilarityMetricEnum.min_max_diff: 1.5,
# })
# model_generator.add_custom_similarity_metric_with_weight(lambda original, compressed: 0.5, 1)

# model_generator.use_constraint_strategy({
#   SimilarityMetricEnum.compression_rate: 5,
#   SimilarityMetricEnum.arithmetic_average: 2,
#   SimilarityMetricEnum.median: 3,
#   SimilarityMetricEnum.min_max_diff: 1.5,
# })
# model_generator.add_custom_similarity_metric_with_constraint(lambda original, compressed: 0.5, 0.6)

score = model_generator.build()
print(f'score: {score}')
