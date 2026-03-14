from pydantic_settings import BaseSettings
from os import getenv

class Settings(BaseSettings):
    MINIO_URL: str = getenv("MINIO_URL", "http://localhost:9000")
    MILVUS_URL:str = getenv("MILVUS_URL","http://localhost:19530")
    collection_name: str = "text_embbeding"
    chunk_size:int = getenv("CHUNK_SIZE", 500)
    think: bool = getenv("ENABLE_THINK", True)
    
settings = Settings()
