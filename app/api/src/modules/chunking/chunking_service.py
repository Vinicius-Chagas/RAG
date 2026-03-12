from langchain_text_splitters import CharacterTextSplitter

class ChunkingService():
    chunk_size = 500

    splitter = CharacterTextSplitter(
        separator="\n\n",              # Primary split point (paragraphs)
        chunk_size=1000,               # Max characters per chunk
        chunk_overlap=200,             # Overlap to avoid context loss at boundaries
        length_function=len,           # Use len() for character count
    )

    def __init__(self):
        pass

    def chunk_it(self,text:str) -> list[str]:
        return self.splitter.split_text(text)
    
