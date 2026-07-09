from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.crud.crud_category import create_category, get_categories
from app.models.user import UserRole
from app.schemas.category import CategoryCreate, CategoryRead

router = APIRouter()


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=201,
    dependencies=[Depends(require_role(UserRole.MODERATOR))],
)
def create_new_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category_in)