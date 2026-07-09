from sqlalchemy.orm import Session

from app.models.schedule import PlaceSchedule
from app.schemas.schedule import PlaceScheduleCreate


def get_schedules_by_place(db: Session, place_id: int) -> list[PlaceSchedule]:
    return db.query(PlaceSchedule).filter(PlaceSchedule.place_id == place_id).all()


def get_schedule_by_day(
    db: Session, place_id: int, day_of_week: str
) -> PlaceSchedule | None:
    return (
        db.query(PlaceSchedule)
        .filter(
            PlaceSchedule.place_id == place_id,
            PlaceSchedule.day_of_week == day_of_week,
        )
        .first()
    )


def upsert_schedule(
    db: Session, schedule_in: PlaceScheduleCreate, place_id: int
) -> PlaceSchedule:
    existing = get_schedule_by_day(db, place_id, schedule_in.day_of_week)
    is_closed_int = 1 if schedule_in.is_closed else 0

    if existing:
        existing.open_time = schedule_in.open_time
        existing.close_time = schedule_in.close_time
        existing.is_closed = is_closed_int
        db.commit()
        db.refresh(existing)
        return existing

    db_schedule = PlaceSchedule(
        day_of_week=schedule_in.day_of_week,
        open_time=schedule_in.open_time,
        close_time=schedule_in.close_time,
        is_closed=is_closed_int,
        place_id=place_id,
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule