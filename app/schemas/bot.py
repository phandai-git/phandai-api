import uuid
from datetime import datetime
from app.models.bot import BotType
from app.schemas.base import BaseSchema


class BotCreate(BaseSchema):
    name: str
    type: BotType
    system_prompt: str | None = None
    pre_query_prompt: str | None = None
    fallback_message: str | None = None
    out_of_hours_message: str | None = None
    allowed_hours_start: int | None = None
    allowed_hours_end: int | None = None
    max_tokens_per_session: int | None = None
    max_tokens_per_month: int | None = None
    monthly_cap_rands: float | None = None
    # WhatsApp
    whatsapp_number: str | None = None
    whatsapp_phone_number_id: str | None = None
    # Widget
    widget_primary_color: str | None = None
    widget_background_color: str | None = None
    widget_text_color: str | None = None
    widget_logo_url: str | None = None
    widget_bot_name: str | None = None
    widget_greeting: str | None = None
    widget_position: str | None = None


class BotUpdate(BaseSchema):
    name: str | None = None
    is_active: bool | None = None
    system_prompt: str | None = None
    pre_query_prompt: str | None = None
    fallback_message: str | None = None
    out_of_hours_message: str | None = None
    allowed_hours_start: int | None = None
    allowed_hours_end: int | None = None
    max_tokens_per_session: int | None = None
    max_tokens_per_month: int | None = None
    monthly_cap_rands: float | None = None
    whatsapp_number: str | None = None
    whatsapp_phone_number_id: str | None = None
    widget_primary_color: str | None = None
    widget_background_color: str | None = None
    widget_text_color: str | None = None
    widget_logo_url: str | None = None
    widget_bot_name: str | None = None
    widget_greeting: str | None = None
    widget_position: str | None = None


class BotResponse(BaseSchema):
    id: uuid.UUID
    business_id: uuid.UUID
    name: str
    type: BotType
    is_active: bool
    system_prompt: str | None
    pre_query_prompt: str | None
    fallback_message: str | None
    out_of_hours_message: str | None
    allowed_hours_start: int | None
    allowed_hours_end: int | None
    max_tokens_per_session: int | None
    max_tokens_per_month: int | None
    tokens_used_this_month: int
    monthly_cap_rands: float | None
    whatsapp_number: str | None
    widget_primary_color: str | None
    widget_background_color: str | None
    widget_text_color: str | None
    widget_logo_url: str | None
    widget_bot_name: str | None
    widget_greeting: str | None
    widget_position: str | None
    created_at: datetime
    updated_at: datetime