from app.util import fast_api_enc_util
from fastapi import HTTPException, Depends, APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from app.models.schemas import UserCreate, ResponseUser
from app.db_config.database import get_db
from sqlalchemy.orm import Session
import app.models.db_models as db_models

router = APIRouter(
    prefix="/users", tags=['users']
)


@router.post("/", status_code=HTTP_201_CREATED,
             response_model=ResponseUser)
def create_user(users: UserCreate, db: Session = Depends(get_db)):
    users.password = fast_api_enc_util.hash(users.password)
    new_user = db_models.User(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id}, not found")
    return user
