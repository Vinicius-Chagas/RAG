from sentence_transformers import SentenceTransformer

class EmbbedingService():

    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    def embbed_it(self, chunks: list[str]):
        return self.model.encode(sentences=chunks)