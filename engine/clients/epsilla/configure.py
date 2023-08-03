import time

from engine.base_client.configure import BaseConfigurator
from engine.clients.epsilla.config import *
from pyepsilla.vectordb import Client


class EpsillaConfigurator(BaseConfigurator):
    def __init__(self, host, collection_params: dict, connection_params: dict):
        super().__init__(host, collection_params, connection_params)
        self.client = Client(host=connection_params.get('host', "127.0.0.1"), port=connection_params.get('port', 8888))
        self.client.load_db(db_name=EPSILLA_DATABASE_NAME, db_path="/tmp/epsilla")
        self.client.use_db(db_name=EPSILLA_DATABASE_NAME)


    def clean(self):
        print("epsilla has already been deleted")

    def recreate(self, distance, vector_size, collection_params, connection_params, extra_columns_name,
                 extra_columns_type):
        print("[EPSILLA] Metric:", DISTANCE_MAPPING[distance])
        print(f"distance {DISTANCE_MAPPING[distance]}, vector_size {vector_size}, collection_params {collection_params}")
        # if EPSILLA_INDEX_NAME in self.client.list_indexes():
        self.client.drop_table(EPSILLA_INDEX_NAME)

        # metadata_config = {
        # "indexed": index_column_list
        # }
        table_fields = [
            {"name": "ID", "dataType": "INT"},
            {"name": "Doc", "dataType": "STRING"},
            {"name": "Embedding", "dataType": "VECTOR_FLOAT", "dimensions": vector_size}
        ]
        self.client.create_table(table_name=EPSILLA_INDEX_NAME,
                                table_fields=table_fields
                              )
        # waiting for index ready
        print("[EPSILLA] sleep 30 ...")
        time.sleep(30)
        # while True:
        #     try:
        #         index_description = pinecone.describe_index(name=EPSILLA_INDEX_NAME)
        #         if index_description.status["ready"] and index_description.status["state"] == "Ready":
        #             print("pinecone index status is Ready!")
        #             break
        #         else:
        #             print(f"index status is not Ready: {index_description.status}")
        #             time.sleep(2)
        #     except Exception as e:
        #         print(f"waiting pinecone index ready: {e}")

    def execution_params(self, distance, vector_size) -> dict:
        return {"normalize": DISTANCE_MAPPING[distance] == Distance.COSINE}
