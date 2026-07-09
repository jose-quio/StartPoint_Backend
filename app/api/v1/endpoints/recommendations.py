from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.place import PlaceRead
from app.services.recommendation_service import get_home_recommendations

router = APIRouter()


@router.get("/home", response_model=list[PlaceRead])
def home_recommendations(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_home_recommendations(db, current_user.id)