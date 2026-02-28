import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.bot import BotCreate, BotUpdate, BotResponse
from app.services.bot import BotService
from app.dependencies import get_current_user

router = APIRouter(prefix="/businesses/{business_id}/bots", tags=["bots"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/", response_model=list[BotResponse])
async def list_bots(
    business_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await BotService.list_by_business(db, business_id, current_user.id)


@router.post("/", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(
    business_id: uuid.UUID,
    payload: BotCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await BotService.create(db, business_id, current_user.id, payload)


@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(
    business_id: uuid.UUID,
    bot_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bot = await BotService.get(db, bot_id, business_id, current_user.id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot


@router.patch("/{bot_id}", response_model=BotResponse)
async def update_bot(
    business_id: uuid.UUID,
    bot_id: uuid.UUID,
    payload: BotUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bot = await BotService.update(db, bot_id, business_id, current_user.id, payload)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot


@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(
    business_id: uuid.UUID,
    bot_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await BotService.soft_delete(db, bot_id, business_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bot not found")