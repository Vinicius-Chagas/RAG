# file_uploader.py MinIO Python SDK example
from minio import Minio
from minio.error import S3Error
from client import client

class MinioService: 

    def list_objects(bucket=str, prefix=str | None):
        return client.list_objects(bucket, prefix)
    
    def list_buckets():
        return client.list_buckets()
    
    def append_object():
        client.append_object()
      