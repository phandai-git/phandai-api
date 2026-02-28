import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.conversation import ConversationResponse, ConversationSummary
from app.services.conversation import ConversationService
from app.dependencies import get_current_user

router = APIRouter(prefix="/businesses/{business_id}", tags=["conversations"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/conversations", response_model=list[ConversationSummary])
async def list_conversations(
    business_id: uuid.UUID,
    bot_id: uuid.UUID | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ConversationService.list_by_business(
        db, business_id, current_user.id, bot_id=bot_id, limit=limit, offset=offset
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    business_id: uuid.UUID,
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = await ConversationService.get(db, conversation_id, business_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get("/bots/{bot_id}/conversations", response_model=list[ConversationSummary])
async def list_bot_conversations(
    business_id: uuid.UUID,
    bot_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await ConversationService.list_by_bot(
        db, bot_id, business_id, current_user.id, limit=limit, offset=offset
    )