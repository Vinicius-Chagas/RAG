from src.bucket.bucket_client import client
from typing import BinaryIO
from fastapi import UploadFile
from minio.datatypes import Object
from typing import Iterator
import time
import os 
from io import BytesIO

class BucketService: 

    def list_objects(self,bucket:str, prefix:str | None) -> Iterator[Object]:
        return client.list_objects(bucket_name=bucket, prefix=prefix)
        
    def get_object(self, file_name:str):
        try:
            response = client.get_object("bronze", file_name)
            return BytesIO(response.read())
        finally:
            response.close()
            response.release_conn()
        
    def list_buckets(self):
        return client.list_buckets()
    
    def add_object(self, bucket:str, file:BytesIO, filename:str):
        obj_name = self.__gen_name(file_name=filename or file.filename)
        client.put_object(bucket_name=bucket, object_name=obj_name, data=file, length=file.getbuffer().nbytes, content_type="pdf")
        return obj_name

    def remove_object(self, bucket:str, obj_name:str):
        client.remove_object(bucket_name=bucket, object_name=obj_name)
      
    def update_object(self, bucket:str, obj_name:str, data:BinaryIO, length:int):
        client.put_object(bucket_name=bucket, object_name=obj_name, data=data, length=length)

    def __gen_name(self, file_name:str):
        root, extension = os.path.splitext(file_name)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return root + timestr + extension