from sqlalchemy.orm import Session

from app.models.place import Place, PlaceStatus
from app.schemas.place import PlaceCreate, PlaceUpdate


def get_place(db: Session, place_id: int) -> Place | None:
    return db.query(Place).filter(Place.id == place_id).first()


def get_places(
    db: Session,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    status: PlaceStatus | None = PlaceStatus.APPROVED,
    skip: int = 0,
    limit: int = 20,
) -> list[Place]:
    query = db.query(Place)

    if status is not None:
        query = query.filter(Place.status == status)
    if category_id is not None:
        query = query.filter(Place.category_id == category_id)
    if min_price is not None:
        query = query.filter(Place.price >= min_price)
    if max_price is not None:
        query = query.filter(Place.price <= max_price)
    if search:
        query = query.filter(Place.name.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


def create_place(db: Session, place_in: PlaceCreate, owner_id: int) -> Place:
    db_place = Place(**place_in.model_dump(), owner_id=owner_id)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


def update_place(db: Session, db_place: Place, place_in: PlaceUpdate) -> Place:
    for field, value in place_in.model_dump(exclude_unset=True).items():
        setattr(db_place, field, value)
    db.commit()
    db.refresh(db_place)
    return db_place


def update_place_status(db: Session, db_place: Place, status: PlaceStatus) -> Place:
    db_place.status = status
    db.commit()
    db.refresh(db_place)
    return db_place


def delete_place(db: Session, db_place: Place) -> None:
    db.delete(db_place)
    db.commit()