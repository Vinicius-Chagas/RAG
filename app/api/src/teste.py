from ollama import Client
from src.db.repository.base_repo import BaseRepo
from src.modules.embbeding.embbeding_service import EmbbedingService
from src.db.client import milvusClient
from src.consts.collection import collection_name

client = Client(host='http://localhost:11435')

repo = BaseRepo(milvusClient)
service = EmbbedingService()

def search(text: list[str]):
    """Convenience wrapper for the two‑step retrieval flow used by the
    Ollama toolchain.

    This function is not used directly in the current script but is kept
    around to demonstrate how a tool could accept plain text, convert it
    into an embedding, and then query the vector store.

    Args:
        text: A list of strings representing the input documents or queries
              that need to be embedded. We pass a list so the underlying
              embedding service can batch the encoding operation.

    Returns:
        The raw output of :meth:`BaseRepo.search`, which is a nested list of
        `SearchItem` objects from Milvus. Each sub-list corresponds to one
        entry in ``text`` and contains the top-k results for that vector.

    Notes:
        - `service.embbed_it` returns a list of floats for each input string.
        - `collection_name` is imported from the project's constants; it
          specifies which Milvus collection is being queried.
        - If this helper is later registered as a tool with Ollama, the
          model can invoke it by passing the ``text`` argument.
    """
    vector = service.embbed_it(text)
    return repo.search(collection_name, vector)

available_tools = {'search':search}

messages = [
    {
        'role': 'user', 
        'content': 'whats written on the paragraph where it says: Can machines think?'
    },
    {
        'role': 'system',
        'content': 'Youre a library assistant. When asked about something search of it using your tools before answering',
    }
]

response = client.chat(
    model='qwen3.5:4b',
    think=True,
    messages=messages,
    tools=[search],  # pass the function directly
)

print("\n\nBefore entering in tool calls: ", response.message)

# Handle tool calls
for tool_call in response.message.tool_calls or []:
    fn = available_tools.get(tool_call.function.name)
    if fn:
        result = fn(**tool_call.function.arguments)
        
        # Send result back to model
        messages.append(response.message)
        print("\n\nfirst prompt", response.message)

        print("\n\n", result)
        messages.append({'role': 'tool', 'content': str(result)})
        
    
        final = client.chat(model='qwen3.5:4b', messages=messages)
        print("\n\nfinal prompt", final.message.content)