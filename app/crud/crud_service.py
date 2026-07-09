from sqlalchemy.orm import Session

from app.models.place import Place
from app.models.schedule import Service
from app.schemas.service import ServiceCreate


def get_services(db: Session) -> list[Service]:
    return db.query(Service).order_by(Service.name).all()


def create_service(db: Session, service_in: ServiceCreate) -> Service:
    db_service = Service(name=service_in.name, icon=service_in.icon)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def assign_services_to_place(
    db: Session, db_place: Place, service_ids: list[int]
) -> Place:
    services = db.query(Service).filter(Service.id.in_(service_ids)).all()
    db_place.services = services
    db.commit()
    db.refresh(db_place)
    return db_place