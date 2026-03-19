from app.infrastructure.repositories.milvus_repo import MilvusRepo
from app.infrastructure.implementations.embbeding.MiniLML12_embbeding import MiniLML12_Embbeding
from app.core.interfaces.embbeding import EmbeddingStrategy
from langchain_core.tools import tool
from app.infrastructure.configs import settings

class SearchService:

    def __init__(self, repo: MilvusRepo, embbeder: EmbeddingStrategy):
        self._repo = repo
        self._embbed = embbeder

    @tool
    def search(self, text: str) -> str:
        """Search the document database for the given text query."""
        vector = self._embbed.embbed_it([text])
        return str(self._repo.search(settings.collection_name, vector))
