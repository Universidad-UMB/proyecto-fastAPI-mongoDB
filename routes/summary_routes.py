from fastapi import APIRouter, Depends
from app.schemas.user_schema import User
from app.services.user_service import decodeAccessToken
from app.services.summary_service import monthlySummary

router = APIRouter()

@router.get("/monthly-summary")
async def summary(currentUser=Depends(decodeAccessToken)):
    return await monthlySummary(currentUser)

