import uuid

from pydantic import BaseModel, EmailStr


class BaseUserCreate(BaseModel):
    email: EmailStr


class UserCreateByPassword(BaseUserCreate):
    user_name: str
    password: str


class UserCreateByGoogle(BaseUserCreate):
    google_id: str


class UserResponse(BaseModel):
    uuid_id: uuid.UUID
