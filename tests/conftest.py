from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv.main import load_dotenv
from app.db_config.database import get_db
import os
from app.db_config.database import Base
import pytest


load_dotenv()

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOSTNAME_QA")}:{os.environ.get("DATABASE_PORT")}/{os.environ.get("DATABASE_NAME_QA")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def create_user(client, request):
    res = client.post(
        "/users/", json={"email": request.param[0], "password": request.param[1]})
    new_user = res.json()
    new_user['password'] = request.param[1]
    return new_user
