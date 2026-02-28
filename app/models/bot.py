import uuid
import enum
from sqlalchemy import String, ForeignKey, Text, Integer, Numeric, Boolean, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, SoftDeleteMixin


class BotType(str, enum.Enum):
    WHATSAPP = "whatsapp"
    WEBCHAT  = "webchat"


class Bot(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "bots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[BotType] = mapped_column(Enum(BotType), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Behaviour config ──
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    pre_query_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    fallback_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    out_of_hours_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Operating hours (24hr, nullable = always on) ──
    allowed_hours_start: Mapped[int | None] = mapped_column(Integer, nullable=True)
    allowed_hours_end: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # ── Usage limits ──
    max_tokens_per_session: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_tokens_per_month: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tokens_used_this_month: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    monthly_cap_rands: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    # ── WhatsApp specific ──
    whatsapp_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    whatsapp_phone_number_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # ── Widget config (webchat specific) ──
    widget_primary_color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    widget_background_color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    widget_text_color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    widget_logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    widget_bot_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    widget_greeting: Mapped[str | None] = mapped_column(Text, nullable=True)
    widget_position: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ── Internal model routing ──
    always_use_sonnet: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sonnet_keywords: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Relationships
    business: Mapped["Business"] = relationship(back_populates="bots")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="bot", cascade="all, delete-orphan")