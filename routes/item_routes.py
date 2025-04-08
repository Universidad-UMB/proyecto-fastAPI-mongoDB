from fastapi import APIRouter, HTTPException
from app.schemas.item_schema import Item
from bson import ObjectId
from bson.errors import InvalidId
from app.db.database import collectionItem
from app.schemas.item_update_schema import ItemUpdate

router = APIRouter()

@router.get("/greeting")
async def greeting():
    return "Hola soy item_routes"

@router.post("/create-item")
async def createItem(item: Item):
    newItem = item.model_dump()
    retult = await collectionItem.items.insert_one(newItem)
    
    return {"Message": "Item creado"}

@router.get("/get-item/{itemId}")
async def getItemById(itemId: str):
    
    try:
        objId = ObjectId(itemId)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Id no valido")
    
    
    itemById = await collectionItem.items.find_one({"_id": objId})
    
    if itemById:
        itemById["id"] = str(itemById["_id"])
        del itemById["_id"]
        return itemById
    
    
@router.get("/get-items")
async def getItems():
    cursor =  await collectionItem.items.find({}).to_list(length=None)
    item_list = []
    
    for items in cursor:
        if items:
            items["id"]= str(items["_id"])
            del items["_id"]
            item_list.append(items)
                    
    return item_list

@router.put("/update-item/{idItem}")
async def putItem(idItem: str, itemBody: ItemUpdate):
    try:
        objId = ObjectId(idItem)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Id no valido")
    
    item =  {k: v for k, v in itemBody.dict().items() if v is not None}
    
    itemUpdate = await collectionItem.items.update_one({"_id": objId}, {"$set": item})
    
    return item 
    
    
@router.delete("/delete-item/{idItem}")
async def deleteItem(idItem: str):
    try:
        objId = ObjectId(idItem)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Id no valido")
    
    item = await collectionItem.items.find_one({"_id": objId})
    
    await collectionItem.items.delete_one({"_id": objId})
    
    return {'message': f'Se elimino correctamente el producto: {item["name"]}'}
    
    
    
    
       
    
    
            
            
    
    
        
    
    
            

 
    
    
    
    
 
    


