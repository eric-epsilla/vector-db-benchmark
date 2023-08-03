from engine.base_client.distances import Distance

EPSILLA_API_KEY = ""
EPSILLA_ENVIRONMENT = "us-east-1-aws"
EPSILLA_INDEX_NAME = "benchmark"

DISTANCE_MAPPING = {
    Distance.L2: "euclidean",
    # Distance.DOT: "dotproduct",
    # Distance.COSINE: "cosine"
}
