from abc import ABC, abstractmethod
from src.bucket.bucket_service import BucketService
from typing import BinaryIO
import io

class Extractor(ABC):

    bucketService = BucketService()
    
    @abstractmethod
    def extract(self, file: BinaryIO) -> list[str]:
        pass

    def save_as_txt(self, text: list[str], name: str):  
        file = io.StringIO()
        file.writelines(text)
        file.filename = name

        self.service.add_object("silver", file.buffer)   