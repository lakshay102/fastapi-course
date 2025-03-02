from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode: True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode: True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode: True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

# class Direction(int, Enum):
#     like_add: 1
#     like_remove: 0

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    # dir: Direction