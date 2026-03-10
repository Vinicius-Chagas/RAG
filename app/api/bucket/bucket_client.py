from minio import Minio

client = Minio("localhost:9001",
    access_key="minioadmin",
    secret_key="minioadmin",
)