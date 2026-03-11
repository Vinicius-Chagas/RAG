from abc import ABC, abstractmethod
from typing import BinaryIO

class Extractor(ABC):

    @abstractmethod
    def extract(self, file: BinaryIO) -> list[str]:
        pass
