from pymilvus import MilvusClient
from app.infrastructure.db.vector_schema import MilvulsSchema
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
        """Perform a vector search against a Milvus collection.

        Args:
            collection: Name of the Milvus collection to query.
            vector: A single embedding (list of floats) or a batch of embeddings.
                    The method expects the vector(s) you obtained from the
                    embedding service. Milvus will compare this against the
                    stored "text_vector" field.

        Returns:
            A nested list of :class:`SearchItem` instances. Each sub-list
            corresponds to one query vector (useful when passing multiple
            vectors at once) and contains the top-k results, ordered by
            increasing distance (smaller is more similar).

        Notes:
            - We hardcode `anns_field` to "text_vector" because that is the
              field name used during indexing in this project.
            - `limit` is currently set to 3 but can be made configurable if
              higher recall is needed.
            - `search_params` sets the metric type to inner product (IP); other
              metrics such as L2 are available depending on model and indexing.
            - `output_fields` restricts the returned payload to just the text
              field. Additional fields (e.g. metadata) should be added here if
              they are indexed and required by consumers.
        """
        return self.client.search(
            collection_name=collection,
            anns_field="text_vector",
            data=vector,
            limit=3,
            search_params={"metric_type": "COSINE"},
            output_fields=["text"]
        )