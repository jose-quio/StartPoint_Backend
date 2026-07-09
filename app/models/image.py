from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class PlaceImage(Base):
    __tablename__ = "place_images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)  # foto principal del lugar
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)

    place = relationship("Place", back_populates="images")