from src.model_generator import ModelGenerator

model_generator = ModelGenerator()
model_generator.set_measurements()
score = model_generator.build()
print(f'score: {score}')
