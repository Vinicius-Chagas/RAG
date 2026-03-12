from pymilvus import DataType
from src.db.client import milvusClient
from src.consts.collection import collection_name
schema = milvusClient.create_schema()

class MilvulsSchema():
    id: str | None
    text_vector: list[float]
    text: str

schema.add_field(
    field_name="id",
    datatype=DataType.VARCHAR,
    is_primary=True,
    auto_id=True
)

schema.add_field(
    field_name="text_vector",
    datatype=DataType.FLOAT_VECTOR,
    dim=384
)

schema.add_field(
    field_name="text",
    datatype=DataType.VARCHAR,
    max_length=256
)

index_params = milvusClient.prepare_index_params()

index_params.add_index(
    field_name="text_vector", 
    index_type="AUTOINDEX",
    metric_type="COSINE"
)

milvusClient.create_collection(
    collection_name=collection_name,
    schema=schema,
    index_params=index_params
)

milvusClient.load_collection(
    collection_name=collection_name
)

res = milvusClient.get_load_state(
    collection_name=collection_name
)


print(res)