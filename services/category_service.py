from fastapi import HTTPException
from app.schemas.user_schema import User
from app.schemas.category_schema import Category
from app.schemas.category_schema_update import CategoryUpdate
from app.db.database import collectionItem
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId



async def createCategory(category: Category, currentUser: User):
    newCategory = category.model_dump()
    
    newCategory["user_id"]=currentUser["_id"]
    newCategory["creationDate"]= datetime.now()
    newCategory["spent"]= 0.0
    newCategory["income"] = 0.0
    newCategory["balance"]= newCategory["budget"] 
    newCategory["name"].lower()
    
    await collectionItem.categories.insert_one(newCategory)
    
    return {"message": f"La categoria {newCategory["name"]} se creo correctamente"}


async def createDefaultCategories(idUser: ObjectId):

    defaultCategories: Category
    
    defaultCategories = [
        {"name": "alimentacion", "budget": 100000.0, "income": 100000.0, "spent": 0.0, "balance":100000.0, "user_id": idUser, "CreationDate": datetime.now()},
        {"name": "transporte", "budget": 100000.0, "income": 100000.0, "spent": 0.0, "balance":100000.0, "user_id": idUser, "CreationDate": datetime.now()},
        {"name": "sueldo", "budget": 100000.0, "income": 100000.0, "spent": 0.0, "balance":100000.0, "user_id": idUser, "CreationDate": datetime.now()},
    ] 
    
    await collectionItem.categories.insert_many(defaultCategories)
    
    
async def updateCategory(currentUser: User, transaction: dict):
    categoryToUpdate = await collectionItem.categories.find_one({"user_id": currentUser["_id"], "name": transaction["category"]})
    
    if transaction["type"] == "gasto":
        categoryToUpdate["spent"] = categoryToUpdate["spent"] + transaction["amount"]
    else:
        categoryToUpdate["income"]= categoryToUpdate["income"] + transaction["amount"]
    
    categoryToUpdate["balance"] = categoryToUpdate["income"] - categoryToUpdate["spent"]
    update = await collectionItem.categories.update_one({"user_id": currentUser["_id"], "name": transaction["category"]}, {"$set": categoryToUpdate}) 
    print(update.upserted_id)
async def updateCategoryByUpdateTransaction(currentUser: User, oldTransaction: dict, transactionUpdate: dict):
    
    ##¿Agregar logica cuando categoria cambia?
    categoryToUpdate = await collectionItem.categories.find_one({"user_id": currentUser["_id"], "name": transactionUpdate["category"]})
 
    if transactionUpdate["type"]== "gasto" and oldTransaction["type"]== "gasto":
        categoryToUpdate["spent"] = (categoryToUpdate["spent"] - oldTransaction["amount"]) + transactionUpdate["amount"]
    elif transactionUpdate["type"] == "ingreso" and oldTransaction["type"]=="gasto":
        categoryToUpdate["spent"] = categoryToUpdate["spent"] - oldTransaction["amount"]
        categoryToUpdate["income"] = categoryToUpdate["income"] + transactionUpdate["amount"] 
    elif transactionUpdate["type"] == "gasto" and oldTransaction["type"] == "ingreso":
        categoryToUpdate["income"] = categoryToUpdate["income"] - oldTransaction["amount"]
        categoryToUpdate["spent"] = categoryToUpdate["spent"] + transactionUpdate["amount"]
    elif transactionUpdate["type"] =="ingreso" and oldTransaction["type"] == "ingreso":
        categoryToUpdate["income"] = (categoryToUpdate["income"] - oldTransaction["amount"]) + transactionUpdate["amount"]
        print("estoy aca")
        
    categoryToUpdate["balance"] = categoryToUpdate["income"] - categoryToUpdate["spent"]  
    update = await collectionItem.categories.update_one({"user_id": currentUser["_id"], "name": transactionUpdate["category"]}, {"$set": categoryToUpdate})
  
    
async def searchCategory(nameCategory:str, currentUser: User):
    
    categoryExist = True
    category = await collectionItem.categories.find_one({"user_id": currentUser["_id"], "name": nameCategory})
    
    if not category:
        categoryExist = False
    
    return categoryExist
    
    
async def getCategories(currentUser: User):
    categories = await collectionItem.categories.find({"user_id": currentUser["_id"]}).to_list(length=None)
    listCategories =[]
    
    for category in categories:
        category["id"] = str(category["_id"])
        category["userid"] = str(category["user_id"]) 
        del category["_id"]
        del category["user_id"]
        listCategories.append(category)
        
    return listCategories

async def categoriesOverBudget(currentUser: User):
    categoriesOver = await collectionItem.categories.find({"$expr": { "$gt": ["$spent", "$budget"]}, "user_id": currentUser["_id"]}).to_list(length=None) 
    
    categoriesOverList = []
    
    if not categoriesOver:
        return {"message": "No hay categorias en las que haya superado el presupuesto fijado"}
    
    for categories in categoriesOver:
        categories["id"]= str(categories["_id"])
        categories["user_id"]= str(categories["user_id"])
        del categories["_id"]
        del categories["user_id"]
        
        categoriesOverList.append(categories)
        
    return categoriesOverList
        
async def updateCategoryByUser(currentUser: User, updateDataCategory: CategoryUpdate, idCategory: str ):
    try:
        objId = ObjectId(idCategory)
    except InvalidId:
        raise HTTPException(status_code=400, detail="No se encontro categpria")
    
    categoryToUpdate = await collectionItem.categories.find_one({"_id": objId})
    
    category = updateDataCategory.model_dump()
    
    if categoryToUpdate["user_id"] != currentUser["_id"]: 
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder este recurso")
    
    
    if category["income"]:
        category["balance"] = category["income"] - category["spent"]
    
    if not category["name"]:
        category["name"] = categoryToUpdate["name"]
    if not category["budget"]:
        category["budget"] = categoryToUpdate["budget"]
    if not category["income"]:
        category["income"] = categoryToUpdate["income"]
    
    await collectionItem.categories.update_one({"_id": objId}, {"$set": category})
    
    return {"message": f"Se actualizo correctamente la categoria {category["name"]}"}