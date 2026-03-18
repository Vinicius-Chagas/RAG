from fastapi import APIRouter, Depends
from app.core.entities.file import File
from io import BytesIO
from fastapi import UploadFile
from app.core.services.chat_service import ChatService
from fastapi import Cookie, Response
from typing import Annotated
import uuid



router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

chatService = ChatService()

@router.post("/message")
def send_message(response: Response, message: str, session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7
        )
    return chatService.send_message(message, session_id)