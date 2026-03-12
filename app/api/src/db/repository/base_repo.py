from pymilvus import MilvusClient
from src.db.schema import MilvulsSchema

class BaseRepo():
    client: MilvusClient
    
    def __init__(self, client: MilvusClient):
        self.client = client

    def insert(self, collection: str, data: list[MilvulsSchema]):
        self.client.insert(
            collection_name=collection,
            data=data
        )