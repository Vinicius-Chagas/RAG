from abc import ABC, abstractmethod
from src.modules.bucket.bucket_service import BucketService
from typing import BinaryIO
from src.dto.file import File
import io
import os

class Extractor(ABC):

    bucketService = BucketService()
    
    @abstractmethod
    def extract(self, file: BinaryIO) -> list[str]:
        pass

    def save_as_txt(self, text: list[str], name: str):  
        file = File( io.BytesIO("/n".join(text).encode("utf-8")), self.__build_txt_name(name), "text")
        self.bucketService.add_object("silver", file)   

    def __build_txt_name(self, name:str):
        name, extension = os.path.splitext(name)
        return name + ".txt"