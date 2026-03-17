from abc import ABC, abstractmethod
from typing import BinaryIO

class ExtractorStrategy(ABC):
    
    @abstractmethod
    def process(self, file: BinaryIO) -> list[str]:
        pass

