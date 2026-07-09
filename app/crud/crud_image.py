from sqlalchemy.orm import Session

from app.models.image import PlaceImage
from app.schemas.image import PlaceImageCreate


def get_images_by_place(db: Session, place_id: int) -> list[PlaceImage]:
    return db.query(PlaceImage).filter(PlaceImage.place_id == place_id).all()


def get_image(db: Session, image_id: int) -> PlaceImage | None:
    return db.query(PlaceImage).filter(PlaceImage.id == image_id).first()


def add_image(db: Session, image_in: PlaceImageCreate, place_id: int) -> PlaceImage:
    if image_in.is_primary:
        # Si esta va a ser la principal, desmarca las demás del mismo lugar
        db.query(PlaceImage).filter(
            PlaceImage.place_id == place_id, PlaceImage.is_primary.is_(True)
        ).update({"is_primary": False})

    db_image = PlaceImage(**image_in.model_dump(), place_id=place_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, db_image: PlaceImage) -> None:
    db.delete(db_image)
    db.commit()