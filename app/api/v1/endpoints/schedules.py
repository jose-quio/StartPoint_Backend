from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.crud_place import get_place
from app.crud.crud_schedule import get_schedules_by_place, upsert_schedule
from app.models.user import User, UserRole
from app.schemas.schedule import PlaceScheduleCreate, PlaceScheduleRead

router = APIRouter()


@router.get("/place/{place_id}", response_model=list[PlaceScheduleRead])
def list_schedules_for_place(place_id: int, db: Session = Depends(get_db)):
    return get_schedules_by_place(db, place_id)


@router.put("/place/{place_id}", response_model=PlaceScheduleRead)
def set_schedule_for_place(
    place_id: int,
    schedule_in: PlaceScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    if db_place.owner_id != current_user.id and current_user.role != UserRole.MODERATOR:
        raise HTTPException(status_code=403, detail="No tienes permisos sobre este lugar")
    return upsert_schedule(db, schedule_in, place_id=place_id)