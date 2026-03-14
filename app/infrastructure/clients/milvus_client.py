from pymilvus import MilvusClient
from core.configs import settings

milvusClient = MilvusClient(settings.MILVUS_URL)