from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class CreatePost(PostBase):
    pass


class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUser

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: Post
    votes: int


class ResponsePost(Post):
    owner_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional['str'] = None


class ResponseVote(BaseModel):
    id: int
    post_id: int
    user_id: int


class CreateVote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)
