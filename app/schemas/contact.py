import uuid
from datetime import datetime
from app.schemas.base import BaseSchema


class ContactCreate(BaseSchema):
    phone: str | None = None
    email: str | None = None
    name: str | None = None
    notes: str | None = None
    metadata_: dict | None = None


class ContactUpdate(BaseSchema):
    phone: str | None = None
    email: str | None = None
    name: str | None = None
    notes: str | None = None
    metadata_: dict | None = None


class ContactResponse(BaseSchema):
    id: uuid.UUID
    business_id: uuid.UUID
    phone: str | None
    email: str | None
    name: str | None
    notes: str | None
    metadata_: dict | None
    created_at: datetime
    updated_at: datetime