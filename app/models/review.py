from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(SmallInteger, nullable=False)  # 1 a 5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)

    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")