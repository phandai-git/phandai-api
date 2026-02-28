import uuid
import enum
from sqlalchemy import String, ForeignKey, Text, Integer, Numeric, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, SoftDeleteMixin


class ConversationType(str, enum.Enum):
    STANDARD = "standard"   # Haiku — billed at R0.80
    COMPLEX  = "complex"    # Sonnet — billed at R1.50


class ModelUsed(str, enum.Enum):
    HAIKU  = "haiku"
    SONNET = "sonnet"


class Conversation(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    bot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bots.id", ondelete="CASCADE"), nullable=False, index=True
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # ── Session ──
    # session_id links to DynamoDB active session for context window
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # ── Exchange ──
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    assistant_response: Mapped[str] = mapped_column(Text, nullable=False)

    # ── Classification ──
    conversation_type: Mapped[ConversationType] = mapped_column(
        Enum(ConversationType), nullable=False
    )
    model_used: Mapped[ModelUsed] = mapped_column(
        Enum(ModelUsed), nullable=False
    )

    # ── Usage ──
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # ── Billing ──
    amount_rands: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    is_billed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    bot: Mapped["Bot"] = relationship(back_populates="conversations")
    contact: Mapped["Contact | None"] = relationship(back_populates="conversations")
    billing_event: Mapped["BillingEvent | None"] = relationship(back_populates="conversation")