from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_role
from app.crud.crud_place import get_place
from app.crud.crud_service import assign_services_to_place, create_service, get_services
from app.models.user import User, UserRole
from app.schemas.place import PlaceRead
from app.schemas.service import PlaceServiceAssign, ServiceCreate, ServiceRead

router = APIRouter()


@router.get("/", response_model=list[ServiceRead])
def list_services(db: Session = Depends(get_db)):
    return get_services(db)


@router.post(
    "/",
    response_model=ServiceRead,
    status_code=201,
    dependencies=[Depends(require_role(UserRole.MODERATOR))],
)
def create_new_service(service_in: ServiceCreate, db: Session = Depends(get_db)):
    return create_service(db, service_in)


@router.put("/place/{place_id}", response_model=PlaceRead)
def assign_place_services(
    place_id: int,
    payload: PlaceServiceAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    if db_place.owner_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=403, detail="No tienes permisos sobre este lugar")
    return assign_services_to_place(db, db_place, payload.service_ids)