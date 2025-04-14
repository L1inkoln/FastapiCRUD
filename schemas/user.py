from typing import Optional
from pydantic import BaseModel


class UserLoginShema(BaseModel):
    username: str
    password: str


# Для создания пользователя
class UserCreate(BaseModel):
    name: str
    age: int
    username: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    username: Optional[str] = None


# Модель для ответа
class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    username: str
