from app.infrastructure.repositories.milvus_repo import MilvusRepo
from app.core.interfaces.embbeding import EmbeddingStrategy
from app.infrastructure.configs import settings
from typing import List, Dict, Any

class SearchService:

    def __init__(self, repo: MilvusRepo, embbeder: EmbeddingStrategy):
        self._repo = repo
        self._embbed = embbeder
        self._last_results: List[Dict[str, Any]] = []

    def search(self, text: str) -> str:
        """Search the document database for the given text query."""
        vector = self._embbed.embbed_it([text])
        raw_results = self._repo.search(settings.collection_name, vector)
        
        self._last_results = []
        if raw_results and len(raw_results) > 0:
            result_group = raw_results[0]
            for idx, item in enumerate(result_group[:3]):
                item_id = item.get("id", f"result_{idx}")
                item_distance = float(item.get("distance", 0))
                
                entity = item.get("entity", {})
                if isinstance(entity, dict):
                    item_text = entity.get("text", "")
                else:
                    item_text = str(entity)
                
                self._last_results.append({
                    "id": item_id,
                    "distance": item_distance,
                    "text": item_text
                })
        
        return str(raw_results)

    def get_last_search_results(self) -> List[Dict[str, Any]]:
        return self._last_results[:3]
