from src.method_selector import MlMethodSelector
from src.measurement_provider import MeasurementProvider
from src.serializer import SenMLCBORSerializer, SenMLJSONSerializer
from sys import getsizeof

method_selector = MlMethodSelector()
method_selector.set_measurements()
score = method_selector.train()
print(score)

measurement_provider = MeasurementProvider()
dataset = measurement_provider.get_random1()[0]
compressed_data, stats, metrics = method_selector.compress_with_best(dataset)
print(stats)

senML_cbor_size_original = getsizeof(SenMLCBORSerializer().serialize(dataset, '/72/', '1/2', metrics))
senML_cbor_size_compressed = getsizeof(SenMLCBORSerializer().serialize(compressed_data, '/72/', '1/2', metrics))
print(senML_cbor_size_original, senML_cbor_size_compressed, senML_cbor_size_original - senML_cbor_size_compressed)

senML_json_size_original = getsizeof(SenMLJSONSerializer().serialize(dataset, '/72/', '1/2', metrics))
senML_json_size_compressed = getsizeof(SenMLJSONSerializer().serialize(compressed_data, '/72/', '1/2', metrics))
print(senML_json_size_original, senML_json_size_compressed, senML_json_size_original - senML_json_size_compressed)
