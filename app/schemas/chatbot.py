from pydantic import BaseModel

from app.schemas.place import PlaceRead


class ChatMessageRequest(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    reply: str
    places: list[PlaceRead] = []