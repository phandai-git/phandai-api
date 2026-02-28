import uuid
from datetime import datetime
from app.models.billing_event import BillingEventType
from app.schemas.base import BaseSchema


class BillingEventResponse(BaseSchema):
    id: uuid.UUID
    business_id: uuid.UUID
    conversation_id: uuid.UUID | None
    event_type: BillingEventType
    amount_rands: float
    description: str | None
    billing_month: str | None
    created_at: datetime


class BillingSummary(BaseSchema):
    billing_month: str
    platform_fee: float
    conversation_charges: float
    total_rands: float
    standard_conversations: int
    complex_conversations: int
    total_conversations: int