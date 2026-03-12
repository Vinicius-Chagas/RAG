from abc import ABC, abstractmethod
from src.modules.extractor.extractor import Extractor
from src.enums.extractor_type import ExtractorType

class ExtractorCreator(ABC):

    @abstractmethod
    def getExtractor(self, type: ExtractorType) -> Extractor | None:
        pass