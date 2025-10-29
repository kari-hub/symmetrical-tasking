from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from .tasks import Task


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    tasks: List[Task] = Field(default_factory=list)

    model_config = {"from_attributes": True}
