from pydantic import BaseModel, ConfigDict

from app.schemas.place import PlaceRead


class FavoriteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place: PlaceRead