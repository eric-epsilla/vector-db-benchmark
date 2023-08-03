from typing import List, Optional, Tuple

from engine.base_client import BaseSearcher
from engine.clients.epsilla.config import *
from engine.clients.epsilla.parser import EpsillaConditionParser
from pyepsilla.vectordb import Client

class EpsillaSearcher(BaseSearcher):
    search_params = {}
    parser = EpsillaConditionParser()
    distance: str = None
    index = None

    @classmethod
    def init_client(
            cls, host: str, distance, connection_params: dict, search_params: dict
    ):
        cls.client = Client(host=connection_params.get('host', "127.0.0.1"), port=connection_params.get('port', 8888))
        cls.client.load_db(db_name=EPSILLA_DATABASE_NAME, db_path="/tmp/epsilla")
        cls.client.use_db(db_name=EPSILLA_DATABASE_NAME)


    @classmethod
    def search_one(cls, vector: List[float], meta_conditions, top: Optional[int], schema) -> List[Tuple[int, float]]:
        while True:
            try:
                status_code, query_response = cls.client.query(
                    table_name=EPSILLA_DATABASE_NAME,
                    query_vector=vector,
                    # query_field="Embedding",
                    query_field=cls.parser.parse(meta_conditions),
                    limit=top
                )
                break
            except Exception as e:
                print(f"epsilla search_one exception 🐛 {e}")
        res_list = []
        for result_op in query_response:
            print(result_op)
            # res_list.append((int(result_op["id"]), float(result_op["score"])))
        print(res_list)
        return res_list
