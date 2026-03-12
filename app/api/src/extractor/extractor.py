from abc import ABC, abstractmethod
from src.bucket.bucket_service import BucketService
from typing import BinaryIO
import io
import os

class Extractor(ABC):

    bucketService = BucketService()
    
    @abstractmethod
    def extract(self, file: BinaryIO) -> list[str]:
        pass

    def save_as_txt(self, text: list[str], name: str):  
        print(len(text))
        buffer = io.BytesIO("/n".join(text).encode("utf-8"))        

        self.bucketService.add_object("silver", buffer, os.path.splitext(name)[0] + ".txt")   