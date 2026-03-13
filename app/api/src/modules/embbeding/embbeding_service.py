from sentence_transformers import SentenceTransformer
import json

class EmbbedingService():

    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device="cpu")

    def embbed_it(self, chunks: list[str]):
        return self.model.encode(sentences=chunks)
    
    def embbed_it_for_model(self, chunks: list[str]):
        """
        Convert a list of text strings into embedding vectors for semantic search.
        
        Args:
            chunks: List of text strings to embed
            
        Returns:
            JSON string containing the embedding vectors
        """
        vectors = self.model.encode(sentences=chunks)
        return json.dumps(vectors.tolist())  # must return a string