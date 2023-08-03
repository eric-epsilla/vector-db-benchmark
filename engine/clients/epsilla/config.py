import random
import string

from engine.base_client.distances import Distance

EPSILLA_DATABASE_NAME = "Benchmark"
EPSILLA_DEFAULT_PORT = "8888"
EPSILLA_DEFAULT_USER = "default"
EPSILLA_DEFAULT_PASSWD = ""

DISTANCE_MAPPING = {
    Distance.L2: "L2",
    # Distance.DOT: "IP",
    # Distance.COSINE: "COSINE"  # cosine problem, when normalized, IP=COSINE
}

H5_COLUMN_TYPES_MAPPING = {
    "float64": "Float64",
    "float32": "Float32",
    "float": "Float64",
    "int32": "Int32",
    "int": "Int32",
    "integer": "Int32",
    "text": "Nullable(String)",  # some text can be null
    "string": "String",
    "blob": "String",
    "geo": "Tuple(Float64, Float64)",  # geo use Point to store, Point == Tuple(Float64, Float64)
    "keyword": "LowCardinality(String)",  # TODO handle ann-filter payload is null
    "boolean": "Boolean",
}


def convert_H52ClickHouseType(h5_column_type: str):
    epsilla_type = H5_COLUMN_TYPES_MAPPING.get(h5_column_type.lower(), None)
    if epsilla_type is None:
        raise RuntimeError(f"🐛 epsilla doesn't support h5 column type: {h5_column_type}")
    return epsilla_type


def get_random_string(length: int):
    random_list = []
    for i in range(length):
        random_list.append(random.choice(string.ascii_uppercase + string.digits))
    return ''.join(random_list)
