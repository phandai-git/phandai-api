import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.analytics import AnalyticsSummary
from app.services.analytics import AnalyticsService
from app.dependencies import get_current_user

router = APIRouter(prefix="/businesses/{business_id}/analytics", tags=["analytics"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/", response_model=AnalyticsSummary)
async def get_analytics(
    business_id: uuid.UUID,
    period: str | None = None,   # e.g. "2026-03" — defaults to current month
    bot_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    summary = await AnalyticsService.get_summary(
        db, business_id, current_user.id, period=period, bot_id=bot_id
    )
    if not summary:
        raise HTTPException(status_code=404, detail="No analytics data found")
    return summary