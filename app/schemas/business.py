import uuid
from datetime import datetime
from pydantic import EmailStr
from app.schemas.base import BaseSchema


class UserCreate(BaseSchema):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserUpdate(BaseSchema):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseSchema):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime