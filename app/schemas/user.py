from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    nickname: str
    password: str


class UserActivated(UserBase):
    id: int
    is_active: bool
    email: EmailStr


class User(UserBase):
    id: int
