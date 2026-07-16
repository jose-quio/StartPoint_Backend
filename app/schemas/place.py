from pydantic import BaseModel, ConfigDict

from app.models.place import PlaceStatus
from app.schemas.category import CategoryRead
from app.schemas.image import PlaceImageRead
from app.schemas.schedule import PlaceScheduleRead
from app.schemas.service import ServiceRead

class PlaceBase(BaseModel):
    name: str
    description: str | None = None
    price: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None
    category_id: int


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None
    category_id: int | None = None


class PlaceStatusUpdate(BaseModel):
    status: PlaceStatus


class PlaceRead(PlaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: PlaceStatus
    owner_id: int
    category: CategoryRead
    images: list[PlaceImageRead] = []
    services: list[ServiceRead] = []
    schedules: list[PlaceScheduleRead] = []
    average_rating: float | None = None
    review_count: int = 0
    is_favorite: bool = False