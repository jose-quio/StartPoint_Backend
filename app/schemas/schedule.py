from datetime import time

from pydantic import BaseModel, ConfigDict

from app.models.schedule import Weekday


class PlaceScheduleBase(BaseModel):
    day_of_week: Weekday
    open_time: time | None = None
    close_time: time | None = None
    is_closed: bool = False


class PlaceScheduleCreate(PlaceScheduleBase):
    pass


class PlaceScheduleRead(PlaceScheduleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place_id: int