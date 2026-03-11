from abc import ABC, abstractmethod

class Abstract_Extractor(ABC):

    @abstractmethod
    def extract(self) -> 1 | 0:
        pass