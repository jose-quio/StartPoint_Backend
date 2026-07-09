from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.crud_review import (
    create_review,
    delete_review,
    get_review,
    get_review_by_user_and_place,
    get_reviews_by_place,
    update_review,
)
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter()


@router.get("/place/{place_id}", response_model=list[ReviewRead])
def list_reviews_for_place(place_id: int, db: Session = Depends(get_db)):
    return get_reviews_by_place(db, place_id)


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_new_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = get_review_by_user_and_place(db, current_user.id, review_in.place_id)
    if existing:
        raise HTTPException(
            status_code=400, detail="Ya dejaste una reseña para este lugar"
        )
    return create_review(db, review_in, user_id=current_user.id)


@router.put("/{review_id}", response_model=ReviewRead)
def update_existing_review(
    review_id: int,
    review_in: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes editar esta reseña")
    return update_review(db, db_review, review_in)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes borrar esta reseña")
    delete_review(db, db_review)