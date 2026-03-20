from typing import Dict, List, Callable, Any, Union
import time
import re
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from app.infrastructure.mlflow_config import start_run, log_metrics, log_params, end_run
from app.api.schemas.chat_response import ChatResponse, SearchResult
from pydantic import BaseModel

Message = Union[HumanMessage, SystemMessage]

class MilvusHit(BaseModel):
    id: str
    distance: float
    text: str
class ToolStep(BaseModel):
    tool: str
    input: str | dict
    result: list[MilvusHit] | str

class ParsedResponse(BaseModel):
    thinking: str
    answer: str
    result: list[MilvusHit] | str

class ChatService:
    chats: Dict[str, List[Message]] = {}
    system_prompt: List[Message] = [
        SystemMessage("You are a library assistant. Always search before answering."),
    ]

    def __init__(self, model: ChatOllama, tools: List[Callable[..., Any]], search_service=None):
        self._agent = model.bind_tools(tools)
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

    def _calculate_confidence_score(self, tool_step: list[ToolStep]) -> float:
        if tool_step:
            avg_distance = sum([r.result.distance or 0 for r in tool_step]) / len(tool_step)
            confidence = max(0.0, min(1.0, 1.0 - avg_distance))
            return confidence
        return 0.0

    def send_message(self, message: str, session_id: str) -> ChatResponse:
        start_time = time.time()
        
        chat = self._get_or_create_chat(session_id)
        chat.append(HumanMessage(content=message))

        result = self.agent.invoke(chat)

        parsed_response = self._parse_agent_output(result)

        response_time = time.time() - start_time
        confidence_score = self._calculate_confidence_score(parsed_response)

        start_run()
        log_params({
            "model_name": "qwen3.5-unsloth",
            "session_id": session_id,
            "message_count": len(chat)
        })
        log_metrics({
            "response_time_seconds": response_time,
            "confidence_score": confidence_score,
            "search_result_count": len(parsed_response.result)
        })
        end_run()

        return ChatResponse(
            search_results=parsed_response.result,
            agent_thoughts=parsed_response.thinking,
            answer=parsed_response.answer,
            response_time_seconds=response_time,
            confidence_score=confidence_score,
            session_id=session_id,
            message_count=len(chat)
        )
    
    def _parse_agent_output(result: dict) -> ParsedResponse:
        raw_output = result.get("output", "")

        think_match = re.search(r"<think>(.*?)</think>", raw_output, re.DOTALL)
        thinking = think_match.group(1).strip() if think_match else None
        answer = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL).strip()

        tool_steps = [
            ToolStep(
                tool=action.tool,
                input=action.tool_input,
                result=str(output),
                distance=action.tool
            )
            for action, output in result.get("intermediate_steps", [])
        ]

        return ParsedResponse(Thinking=thinking, answer=answer, tool_steps=tool_steps)



