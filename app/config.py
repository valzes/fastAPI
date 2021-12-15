from pydantic import BaseSettings


class Settings(BaseSettings):
    algorithm: str


class Config:
    env_file = ".env"


settings = Settings()
