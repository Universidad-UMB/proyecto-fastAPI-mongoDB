from fastapi import HTTPException
from app.schemas.transaction_schema import Transaction
from app.services import category_service
from app.schemas.user_schema import User
from app.schemas.transaction_update_schema import UpdateTransaction
from app.db.database import collectionItem
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

async def registerTransaction(transaction: Transaction, currentUser: User):
    newTransaction = transaction.model_dump()
    newTransaction["id_user"] = currentUser["_id"]
    newTransaction["date"] = datetime.now()
    
    
    existCategory = await category_service.searchCategory(newTransaction["category"], currentUser)
    
    if not existCategory:
        raise HTTPException(status_code=400, detail="No se encontro categoria, ingrese una categoria valida")
    
    await category_service.updateCategory(currentUser, newTransaction)
    await collectionItem.transactions.insert_one(newTransaction)
    
    
    return {"message": "Se registro correctamente la transaccion",
            "Transaction": newTransaction["description"]}

async def getTransactions(currentUser: User):
    transactions = await collectionItem.transactions.find({"id_user": currentUser["_id"]}).to_list(length=None)
    
    listTransactions = []
    
    for transaction in transactions :
        if transactions :
            transaction ["id"] = str(transaction ["_id"])
            transaction ["iduser"] = str(transaction ["id_user"])
            del transaction["_id"]
            del transaction["id_user"]
            listTransactions.append(transaction)
    
    return listTransactions

async def updateTransaction(transaction: UpdateTransaction, idTransaction: str, currentUser: User):
    try:
        objId = ObjectId(idTransaction)
    except InvalidId:
        raise HTTPException(status_code=400, detail="No se encontro transaccion")
    
    oldTransaction= await collectionItem.transactions.find_one({"_id": objId})
    
    
    if oldTransaction["id_user"] != currentUser["_id"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder este recurso")
     
    
    transactionUpdate = transaction.model_dump()
    
    
    
    existCategory = await category_service.searchCategory(transactionUpdate["category"], currentUser)
    
    if not existCategory:
        raise HTTPException(status_code=400, detail="No se encontro categoria, ingrese una categoria valida")
    
    await category_service.updateCategoryByUpdateTransaction(currentUser, oldTransaction, transactionUpdate)    
    await collectionItem.transactions.update_one({"_id": objId}, {"$set": transactionUpdate})
    return {"message": f"Se actualizo correctamente la transaccion: {transactionUpdate["description"]}"}
    
async def deleteTransaction(idTransaction: str, currentUser: User):
    try:
        objId = ObjectId(idTransaction)
    except InvalidId:
        raise HTTPException(status_code=400, detail="No se encontro transaccion")
    
    transactionToDelete = await collectionItem.transactions.find_one({"_id": objId})
    
    if transactionToDelete["id_user"] != currentUser["_id"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder el recurso")
    
    await collectionItem.transactions.delete_one({"_id":objId})
    
    return {"message": f"Se elimino correctamente la transaccion: {transactionToDelete["description"]} "}
    
    
    