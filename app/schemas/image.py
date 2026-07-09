from pydantic import BaseModel, ConfigDict, field_validator


class PlaceImageBase(BaseModel):
    url: str
    is_primary: bool = False

    @field_validator("url")
    @classmethod
    def validate_cloudinary_url(cls, v: str) -> str:
        if "res.cloudinary.com" not in v:
            raise ValueError("La URL debe provenir de Cloudinary")
        return v


class PlaceImageCreate(PlaceImageBase):
    pass


class PlaceImageRead(PlaceImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place_id: int