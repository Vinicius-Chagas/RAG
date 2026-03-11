from src.extraction.extractor_creator import ExtractorCreator
from src.extraction.extractor import Extractor

class ExtractorFactory(ExtractorCreator):

    def getExtractor(self, type: str) -> Extractor:
        match type:
            case "pdf":
                return 1
