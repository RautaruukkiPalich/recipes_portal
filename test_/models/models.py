from typing import List
from pydantic import BaseModel, Field


class Roles(BaseModel):
    id: int
    role_name: str


class User(BaseModel):
    id: int
    nickname: str = Field(min_length=3)


class UserInfo(User):
    name: str
    surname: str
    status: str = Field(min_length=2)
    role: List[Roles]
