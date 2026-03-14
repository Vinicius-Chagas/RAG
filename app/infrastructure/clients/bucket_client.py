from minio import Minio
from core.configs import settings

client = Minio(
    settings.MINIO_URL,
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)
