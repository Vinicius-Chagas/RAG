from minio import Minio
import os

client = Minio(
    os.environ["MINIO_URL"] or "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)
