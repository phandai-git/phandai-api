import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.billing import BillingEventResponse, BillingSummary
from app.services.billing import BillingService
from app.dependencies import get_current_user

router = APIRouter(prefix="/businesses/{business_id}/billing", tags=["billing"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/", response_model=list[BillingSummary])
async def list_billing_summaries(
    business_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await BillingService.list_summaries(db, business_id, current_user.id)


@router.get("/current", response_model=BillingSummary)
async def get_current_month(
    business_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    summary = await BillingService.get_current_month(db, business_id, current_user.id)
    if not summary:
        raise HTTPException(status_code=404, detail="No billing data found")
    return summary


@router.get("/events", response_model=list[BillingEventResponse])
async def list_billing_events(
    business_id: uuid.UUID,
    billing_month: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await BillingService.list_events(
        db, business_id, current_user.id, billing_month=billing_month, limit=limit, offset=offset
    )