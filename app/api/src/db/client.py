from pymilvus import MilvusClient
import os

milvusClient = MilvusClient(os.environ["MILVUS_URL"] or "localhost:19530")