from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.crud_image import add_image, delete_image, get_image, get_images_by_place
from app.crud.crud_place import get_place
from app.models.user import User, UserRole
from app.schemas.image import PlaceImageCreate, PlaceImageRead

router = APIRouter()


@router.get("/place/{place_id}", response_model=list[PlaceImageRead])
def list_images_for_place(place_id: int, db: Session = Depends(get_db)):
    return get_images_by_place(db, place_id)


@router.post(
    "/place/{place_id}", response_model=PlaceImageRead, status_code=status.HTTP_201_CREATED
)
def add_image_to_place(
    place_id: int,
    image_in: PlaceImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    if db_place.owner_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=403, detail="No tienes permisos sobre este lugar")
    return add_image(db, image_in, place_id=place_id)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_place_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_image = get_image(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    db_place = get_place(db, db_image.place_id)
    if db_place.owner_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=403, detail="No tienes permisos sobre este lugar")
    delete_image(db, db_image)