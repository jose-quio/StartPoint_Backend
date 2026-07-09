from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.crud_favorite import (
    add_favorite,
    get_favorite,
    get_favorites_by_user,
    remove_favorite,
)
from app.models.user import User
from app.schemas.favorite import FavoriteRead

router = APIRouter()


@router.get("/", response_model=list[FavoriteRead])
def list_my_favorites(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_favorites_by_user(db, current_user.id)


@router.post("/{place_id}", response_model=FavoriteRead, status_code=status.HTTP_201_CREATED)
def add_place_to_favorites(
    place_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = get_favorite(db, current_user.id, place_id)
    if existing:
        raise HTTPException(status_code=400, detail="Ya está en tus favoritos")
    return add_favorite(db, user_id=current_user.id, place_id=place_id)


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_place_from_favorites(
    place_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_favorite = get_favorite(db, current_user.id, place_id)
    if not db_favorite:
        raise HTTPException(status_code=404, detail="No estaba en tus favoritos")
    remove_favorite(db, db_favorite)