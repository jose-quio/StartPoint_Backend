from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


def get_review(db: Session, review_id: int) -> Review | None:
    return db.query(Review).filter(Review.id == review_id).first()


def get_reviews_by_place(db: Session, place_id: int) -> list[Review]:
    return db.query(Review).filter(Review.place_id == place_id).all()


def get_review_by_user_and_place(
    db: Session, user_id: int, place_id: int
) -> Review | None:
    return (
        db.query(Review)
        .filter(Review.user_id == user_id, Review.place_id == place_id)
        .first()
    )


def create_review(db: Session, review_in: ReviewCreate, user_id: int) -> Review:
    db_review = Review(**review_in.model_dump(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(db: Session, db_review: Review, review_in: ReviewUpdate) -> Review:
    for field, value in review_in.model_dump(exclude_unset=True).items():
        setattr(db_review, field, value)
    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review(db: Session, db_review: Review) -> None:
    db.delete(db_review)
    db.commit()