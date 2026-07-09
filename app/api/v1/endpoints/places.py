from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_role
from app.crud.crud_place import (
    create_place,
    delete_place,
    get_place,
    get_places,
    update_place,
    update_place_status,
)
from app.models.place import PlaceStatus
from app.models.user import User, UserRole
from app.schemas.place import PlaceCreate, PlaceRead, PlaceStatusUpdate, PlaceUpdate

router = APIRouter()


@router.get("/", response_model=list[PlaceRead])
def list_places(
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    # Público: solo ve lugares aprobados
    return get_places(
        db,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        search=search,
        status=PlaceStatus.APPROVED,
        skip=skip,
        limit=limit,
    )


@router.get("/{place_id}", response_model=PlaceRead)
def get_place_detail(place_id: int, db: Session = Depends(get_db)):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return db_place


@router.post(
    "/",
    response_model=PlaceRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(UserRole.PLACE_ADMIN, UserRole.MODERATOR))],
)
def create_new_place(
    place_in: PlaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_place(db, place_in, owner_id=current_user.id)


@router.put("/{place_id}", response_model=PlaceRead)
def update_existing_place(
    place_id: int,
    place_in: PlaceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    if db_place.owner_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=403, detail="No tienes permisos sobre este lugar")
    return update_place(db, db_place, place_in)


@router.patch(
    "/{place_id}/status",
    response_model=PlaceRead,
    dependencies=[Depends(require_role(UserRole.MODERATOR))],
)
def moderate_place(
    place_id: int, status_in: PlaceStatusUpdate, db: Session = Depends(get_db)
):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return update_place_status(db, db_place, status_in.status)


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_place(
    place_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    if db_place.owner_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=403, detail="No tienes permisos sobre este lugar")
    delete_place(db, db_place)