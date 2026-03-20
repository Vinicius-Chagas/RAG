import sys
import os

# Ensure the app module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymilvus import MilvusClient
from app.infrastructure.configs import settings
from app.infrastructure.repositories.milvus_repo import MilvusRepo
from app.infrastructure.implementations.embbeding.MiniLML12_embbeding import MiniLML12_Embbeding
from app.core.services.search_service import SearchService

def run_test_search(query: str):
    print(f"Initializing search for: '{query}'...")
    
    # 1. Initialize dependencies
    # Using the URL from settings
    client = MilvusClient(uri=settings.MILVUS_URL)
    repo = MilvusRepo(client)
    embedder = MiniLML12_Embbeding()
    
    # 2. Initialize SearchService
    search_service = SearchService(repo, embedder)
    
    # 3. Perform search
    print("Searching Milvus...")
    try:
        results = search_service.search(query)
        
        # 4. Print results
        print("\n--- Search Results ---")
        if not results:
            print("No results found.")
        else:
            # Note: MilvusRepo.search returns a list of results
            # Based on the implementation, it might be a list of lists or a list of SearchItems
            print(results)
        print("----------------------\n")
            
    except Exception as e:
        print(f"An error occurred during search: {e}")

if __name__ == "__main__":
    test_query = "O que é RAG?"
    if len(sys.argv) > 1:
        test_query = " ".join(sys.argv[1:])
    
    run_test_search(test_query)
