from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    icon: str | None = None


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PlaceServiceAssign(BaseModel):
    service_ids: list[int]