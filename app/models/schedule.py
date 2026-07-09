import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table, Time
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Weekday(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class PlaceSchedule(Base):
    __tablename__ = "place_schedules"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Enum(Weekday), nullable=False)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    is_closed = Column(Integer, default=0)  # 0=abierto, 1=cerrado ese día

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)

    place = relationship("Place", back_populates="schedules")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # "Piscina", "Parrillas", etc.
    icon = Column(String(100), nullable=True)

    places = relationship(
        "Place", secondary="place_services", back_populates="services"
    )


# Tabla intermedia (muchos a muchos) entre Place y Service
place_services = Table(
    "place_services",
    Base.metadata,
    Column("place_id", ForeignKey("places.id"), primary_key=True),
    Column("service_id", ForeignKey("services.id"), primary_key=True),
)