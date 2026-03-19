from typing import Dict, List, Callable, Any, Union
import time
import json

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from app.infrastructure.mlflow_config import start_run, log_metrics, log_params, end_run
from app.api.schemas.chat_response import ChatResponse, SearchResult

Message = Union[HumanMessage, SystemMessage]

class ChatService:
    chats: Dict[str, List[Message]] = {}
    system_prompt: List[Message] = [
        SystemMessage("You are a library assistant. Always search before answering."),
    ]

    def __init__(self, model: ChatOllama, tools: List[Callable[..., Any]], search_service=None):
        self._agent = create_agent(model, tools=tools)
        self._search_service = search_service

    @property
    def agent(self) -> Any:
        return self._agent

    def _get_or_create_chat(self, session_id: str) -> List[Message]:
        chat = self.chats.get(session_id)
        if chat is None:
            chat = list(self.system_prompt)
            self.chats[session_id] = chat
        return chat

    def _extract_search_results(self) -> List[SearchResult]:
        if not self._search_service:
            return []
        
        raw_results = self._search_service.get_last_search_results()
        search_results = []
        
        for idx, item in enumerate(raw_results[:3]):
            search_results.append(SearchResult(
                id=item.get("id", f"result_{idx}"),
                distance=item.get("distance", 0),
                text=item.get("text", "")
            ))
        
        return search_results

    def _extract_thinking(self, result: dict) -> str:
        for msg in result.get("messages", []):
            if hasattr(msg, "response_metadata"):
                if isinstance(msg.response_metadata, dict):
                    if "thinking" in msg.response_metadata:
                        return msg.response_metadata["thinking"]
        
        last_msg = result.get("messages", [])[-1] if result.get("messages") else None
        if last_msg and hasattr(last_msg, "content") and isinstance(last_msg.content, str):
            if "<think>" in last_msg.content:
                start_idx = last_msg.content.find("<think>") + 7
                end_idx = last_msg.content.find("</think>")
                if end_idx > start_idx:
                    return last_msg.content[start_idx:end_idx].strip()
        
        return ""

    def _extract_answer(self, result: dict) -> str:
        last_msg = result.get("messages", [])[-1]
        content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
        
        if "</think>" in content:
            return content.split("</think>", 1)[1].strip()
        return content

    def _calculate_confidence_score(self, result: dict, search_results: List[SearchResult]) -> float:
        if search_results:
            avg_distance = sum([r.distance or 0 for r in search_results]) / len(search_results)
            confidence = max(0.0, min(1.0, 1.0 - avg_distance))
            return confidence
        return 0.95

    def send_message(self, message: str, session_id: str) -> ChatResponse:
        start_time = time.time()
        
        chat = self._get_or_create_chat(session_id)
        chat.append(HumanMessage(message))

        result = self.agent.invoke({"messages": chat})

        response_time = time.time() - start_time
        search_results = self._extract_search_results()
        agent_thoughts = self._extract_thinking(result)
        answer = self._extract_answer(result)
        confidence_score = self._calculate_confidence_score(result, search_results)

        start_run()
        log_params({
            "model_name": "qwen3.5-unsloth",
            "session_id": session_id,
            "message_count": len(chat)
        })
        log_metrics({
            "response_time_seconds": response_time,
            "confidence_score": confidence_score,
            "search_result_count": len(search_results)
        })
        end_run()

        return ChatResponse(
            search_results=search_results,
            agent_thoughts=agent_thoughts,
            answer=answer,
            response_time_seconds=response_time,
            confidence_score=confidence_score,
            session_id=session_id,
            message_count=len(chat)
        )


