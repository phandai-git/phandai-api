import uuid
import enum
from sqlalchemy import String, ForeignKey, Text, Numeric, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, SoftDeleteMixin


class BillingEventType(str, enum.Enum):
    CONVERSATION     = "conversation"      # per-conversation charge
    MONTHLY_PLATFORM = "monthly_platform"  # R299 flat fee
    CREDIT           = "credit"            # manual credit applied


class BillingEvent(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "billing_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True
    )

    # ── Event detail ──
    event_type: Mapped[BillingEventType] = mapped_column(Enum(BillingEventType), nullable=False)
    amount_rands: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Period (for monthly platform fee) ──
    billing_month: Mapped[str | None] = mapped_column(String(7), nullable=True)  # e.g. "2026-03"

    # Relationships
    business: Mapped["Business"] = relationship(back_populates="billing_events")
    conversation: Mapped["Conversation | None"] = relationship(back_populates="billing_event")