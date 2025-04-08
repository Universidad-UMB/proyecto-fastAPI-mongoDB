from fastapi import APIRouter, Depends
from schemas.user_schema import User
from services.user_service import decodeAccessToken
from services.summary_service import monthlySummary

router = APIRouter()

@router.get("/monthly-summary")
async def summary(currentUser=Depends(decodeAccessToken)):
    return await monthlySummary(currentUser)

