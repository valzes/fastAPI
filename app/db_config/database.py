from dotenv.main import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOSTNAME")}:{os.environ.get("DATABASE_PORT")}/{os.environ.get("DATABASE_NAME")}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
