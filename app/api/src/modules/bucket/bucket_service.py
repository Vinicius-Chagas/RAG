from src.modules.bucket.bucket_client import client
from typing import BinaryIO
from minio.datatypes import Object
from typing import Iterator
from src.dto.file import File
import time
import os 
from io import BytesIO

class BucketService: 

    def list_objects(self,bucket:str, prefix:str | None) -> Iterator[Object]:
        return client.list_objects(bucket_name=bucket, prefix=prefix)
        
    def get_object(self, file_name:str, bucket:str = "bronze"):
        response = None
        try:
            response = client.get_object(bucket, file_name)
            return BytesIO(response.read())
        finally:
            if response is not None:
                response.close()
                response.release_conn()
        
    def list_buckets(self):
        return client.list_buckets()
    
    def add_object(self, bucket:str, file: File):
        obj_name = self.__gen_name(file_name=file.filename)
        client.put_object(bucket_name=bucket, object_name=obj_name, data=file.data, length=file.size, content_type=file.content_type)
        return obj_name

    def remove_object(self, bucket:str, obj_name:str):
        client.remove_object(bucket_name=bucket, object_name=obj_name)
      
    def update_object(self, bucket:str, obj_name:str, data:BinaryIO, length:int):
        client.put_object(bucket_name=bucket, object_name=obj_name, data=data, length=length)

    def __gen_name(self, file_name:str):
        root, extension = os.path.splitext(file_name)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return root + timestr + extension