from fastapi import Depends, APIRouter, status, HTTPException
from app.db_config.database import get_db
from sqlalchemy.orm import Session
from app.models.schemas import Token
import app.models.db_models as db_models
from app.util import fast_api_enc_util
from app.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(
        db_models.User.email == user_credentials.username).first()
    print(user_credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not fast_api_enc_util.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password")

    token = create_access_token(data={"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}
