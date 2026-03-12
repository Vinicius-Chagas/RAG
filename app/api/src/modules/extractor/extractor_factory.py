from src.modules.extractor.extractor_creator import ExtractorCreator
from src.modules.extractor.extractor import Extractor
from src.modules.extractor.pdf_extractor import PDFExtractor
from src.enums.extractor_type import ExtractorType

class ExtractorFactory(ExtractorCreator):

    def getExtractor(self, type: ExtractorType) -> Extractor | None:
        match type:
            case "pdf":
                return PDFExtractor()
        
        return None
