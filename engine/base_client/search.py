import functools
import time
from multiprocessing import get_context
from typing import List, Optional, Tuple

import numpy as np
import tqdm

DEFAULT_TOP = 100


class BaseSearcher:
    MP_CONTEXT = None

    def __init__(self, host, connection_params, search_params):
        self.host = host
        self.connection_params = connection_params
        self.search_params = search_params

    @classmethod
    def init_client(cls, host: str, distance, connection_params: dict, search_params: dict):
        raise NotImplementedError()

    @classmethod
    def get_mp_start_method(cls):
        return None

    @classmethod
    def search_one(
            cls, vector: List[float], meta_conditions, top: Optional[int], schema: Optional[dict]
    ) -> List[Tuple[int, float]]:
        raise NotImplementedError()

    @classmethod
    def _search_one(cls, query, top: Optional[int] = None, schema: Optional[dict] = None):
        if top is None:
            top = (
                len(query.expected_result)
                if query.expected_result is not None and len(query.expected_result) > 0
                else DEFAULT_TOP
            )

        start = time.perf_counter()
        search_res = cls.search_one(query.vector, query.meta_conditions, top, schema)
        end = time.perf_counter()
        
        # print("======query.vector:", query.vector)

        # Updating the TopK, the number of standard answers contained in the dataset may be less than TopK
        # The HNM dataset only has 25 standard answers.
        ans_len = len(query.expected_result)
        top = (top > ans_len and ans_len or top)

        precision = 1.0
        if query.expected_result is not None:
            # Retrieve the top K results of vector search
            ids = set([x[0] for x in search_res][:top])
            # print("======ids:", ids)
            # Calculate accuracy
            # print("======expected:", query.expected_result[:top])
            precision = len(ids.intersection(query.expected_result[:top])) / top  
            print("======precision:", precision)
        return precision, end - start

    def search_all(
            self,
            distance,
            get_queries,
            queries,  # The number of vectors used for search in each round of testing.
            schema    # Payload fields of dataset
    ):
        parallel = self.search_params.get("parallel", 1)
        top = self.search_params.get("top", None)

        # weaviate-client setup_search may require initialized client
        self.setup_search(self.host, distance, self.connection_params, self.search_params)

        search_one = functools.partial(self.__class__._search_one, top=top, schema=schema)

        queries_need = 1000 * parallel
        # Ensure each process searches at least 1K vectors and all test vectors provided by the dataset are searched.
        count = queries if queries_need <= queries else queries_need
        # Match the correct dataset based on the `query_meta` provided by the `search_parameters`.
        multi_queries = get_queries(times=count, query_meta=self.search_params.get("query_meta", None))
        print(f"parallel - {parallel}, queries have {queries}, queries need {queries_need}, queries run - {count}")
        start = time.perf_counter()

        ctx = get_context(self.get_mp_start_method())
        with ctx.Pool(
                processes=parallel,
                initializer=self.__class__.init_client,
                initargs=(
                        self.host,
                        distance,
                        self.connection_params,
                        self.search_params,
                ),
        ) as pool:
            precisions, latencies = list(
                zip(*pool.imap_unordered(search_one, iterable=tqdm.tqdm(multi_queries)))
            )

        total_time = time.perf_counter() - start
        res = {
            "total_time": total_time,
            "mean_time": np.mean(latencies),
            "mean_precisions": np.mean(precisions),
            "std_time": np.std(latencies),
            "min_time": np.min(latencies),
            "max_time": np.max(latencies),
            "rps": len(latencies) / total_time,
            "p95_time": np.percentile(latencies, 95),
            "p99_time": np.percentile(latencies, 99),
            "precisions": precisions,
            "latencies": latencies,
        }
        # print("[RESULT]:", res)
        return res

    def setup_search(self, host, distance, connection_params: dict, search_params: dict):
        pass

    def post_search(self):
        pass
