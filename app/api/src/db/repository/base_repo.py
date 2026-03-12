from pymilvus import MilvusClient
from src.db.schema import MilvulsSchema
from typing import TypedDict

class Entity(TypedDict):
    text: str

class SearchItem():
    id: str
    distance: float
    entity: Entity
class BaseRepo():
    client: MilvusClient
    
    def __init__(self, client: MilvusClient):
        self.client = client

    def insert(self, collection: str, data: list[MilvulsSchema]):
        self.client.insert(
            collection_name=collection,
            data=data
        )

    def search(self, collection: str, vector: list[float]) -> list[list[SearchItem]]:
        return self.client.search(
            collection_name=collection,
            anns_field="text_vector",
            data=vector,
            limit=3,
            search_params={"metric_type": "IP"},
            output_fields=["text"]
        )