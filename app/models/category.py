from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)   # Ej: "Piscinas", "Termales"
    icon = Column(String(100), nullable=True)                  # nombre/url del icono

    places = relationship("Place", back_populates="category")