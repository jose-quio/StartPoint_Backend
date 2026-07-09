from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.chatbot import ChatMessageRequest, ChatMessageResponse
from app.services.chatbot_service import get_chatbot_response

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
def chat_with_bot(
    payload: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reply, places = get_chatbot_response(db, current_user.id, payload.message)
    return ChatMessageResponse(reply=reply, places=places)