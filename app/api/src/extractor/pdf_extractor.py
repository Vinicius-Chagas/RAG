from src.extractor.extractor import Extractor
from pypdf import PdfReader
from typing import BinaryIO

class PDFExtractor(Extractor):

    def extract(self, file: BinaryIO) -> list[str]:
        reader = PdfReader(file)
        text: list[str] = []
        for page in reader.pages:
            text.append(page.extract_text(0))

        return text