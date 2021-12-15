import os
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from db_config.database import get_db
from sqlalchemy.orm.session import Session
from models import schemas
from fastapi.security import OAuth2PasswordBearer
from models import db_models
from dotenv import load_dotenv
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRATION"))


def create_access_token(data: dict):
    data_encoded = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_encoded.update({"exp": expiry})
    encoded_jwt = jwt.encode(data_encoded, algorithm=ALGORITHM, key=SECRET_KEY)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    print('verifying access token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(db_models.User).filter(
        db_models.User.id == token_data.id).first()

    return user
