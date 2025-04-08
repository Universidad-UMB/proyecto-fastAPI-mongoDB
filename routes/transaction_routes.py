from fastapi import APIRouter, Depends
from app.schemas.transaction_schema import Transaction
from app.schemas.transaction_update_schema import UpdateTransaction
from app.services.user_service import decodeAccessToken 
from app.services import transaction_service


router = APIRouter()

@router.get("/greeting")
def greeting():
    return {"message": "Hello world transaction"}

@router.post("/new-transaction")
async def newTransaction(transaction: Transaction, user = Depends(decodeAccessToken)):
    return  await transaction_service.registerTransaction(transaction, user)

@router.get("/get-transactions")
async def getTransactions(currentUser = Depends(decodeAccessToken)):
    return await transaction_service.getTransactions(currentUser)

@router.put("/update-transaction/{idTransaction}")
async def updateTransaction( transaction: UpdateTransaction, idTransaction: str, currentUser = Depends(decodeAccessToken)):
    return await transaction_service.updateTransaction(transaction, idTransaction, currentUser)

@router.delete("/delete-transaction/{idTransaction}")
async def deleteTransaction(idTransaction: str, currentUser = Depends(decodeAccessToken)):
    return await transaction_service.deleteTransaction(idTransaction, currentUser)

