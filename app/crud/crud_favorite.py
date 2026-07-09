from sqlalchemy.orm import Session

from app.models.favorite import Favorite


def get_favorites_by_user(db: Session, user_id: int) -> list[Favorite]:
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


def get_favorite(db: Session, user_id: int, place_id: int) -> Favorite | None:
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id, Favorite.place_id == place_id)
        .first()
    )


def add_favorite(db: Session, user_id: int, place_id: int) -> Favorite:
    db_favorite = Favorite(user_id=user_id, place_id=place_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def remove_favorite(db: Session, db_favorite: Favorite) -> None:
    db.delete(db_favorite)
    db.commit()