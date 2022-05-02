from src.model_generator import ModelGenerator
from src.metric import SingleMetricEnum, ComparationMetricEnum

model_generator = ModelGenerator()
model_generator.set_measurements()
model_generator.set_metrics(
  [
    SingleMetricEnum.arithmetic_average,
    SingleMetricEnum.median,
    SingleMetricEnum.min_max_diff,
  ],
  [
    ComparationMetricEnum.arithmetic_average,
    ComparationMetricEnum.median,
    ComparationMetricEnum.min_max_diff,
  ],
)
score = model_generator.build()
print(f'score: {score}')
