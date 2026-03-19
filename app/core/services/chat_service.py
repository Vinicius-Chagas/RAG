from typing import Dict, List, Callable, Any, Union

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

Message = Union[HumanMessage, SystemMessage]


class ChatService:
    chats: Dict[str, List[Message]] = {}
    system_prompt: List[Message] = [
        SystemMessage("You are a library assistant. Always search before answering."),
    ]

    def __init__(self, model: ChatOllama, tools: List[Callable[..., Any]]):
        self._agent = create_agent(model, tools=tools)

    @property
    def agent(self) -> Any:
        return self._agent

    def _get_or_create_chat(self, session_id: str) -> List[Message]:
        chat = self.chats.get(session_id)
        if chat is None:
            chat = list(self.system_prompt)
            self.chats[session_id] = chat

        return chat

    def _find_tool_call(self, result: dict) -> None:
        for msg in result.get("messages", []):
            role = msg.__class__.__name__
            content = msg.content or getattr(msg, "tool_calls", "")
            print(f"[{role}]: {content}\n")


    def send_message(self, message: str, session_id: str) -> str:
        chat = self._get_or_create_chat(session_id)
        chat.append(HumanMessage(message))

        print("Total messages of chat: ", len(chat))

        result = self.agent.invoke({"messages": chat})

        self._find_tool_call(result)

        print(result["messages"][-1].content)
        return result["messages"][-1].content


