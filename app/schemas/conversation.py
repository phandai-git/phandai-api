import uuid
from datetime import datetime
from app.models.conversation import ConversationType, ModelUsed
from app.schemas.base import BaseSchema


class ConversationResponse(BaseSchema):
    id: uuid.UUID
    bot_id: uuid.UUID
    contact_id: uuid.UUID | None
    session_id: str
    user_message: str
    assistant_response: str
    conversation_type: ConversationType
    model_used: ModelUsed
    input_tokens: int
    output_tokens: int
    total_tokens: int
    amount_rands: float
    is_billed: bool
    created_at: datetime


class ConversationSummary(BaseSchema):
    id: uuid.UUID
    bot_id: uuid.UUID
    contact_id: uuid.UUID | None
    conversation_type: ConversationType
    model_used: ModelUsed
    total_tokens: int
    amount_rands: float
    created_at: datetime