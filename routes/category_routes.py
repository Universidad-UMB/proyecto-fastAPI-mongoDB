from fastapi import APIRouter, Depends
from app.services.user_service import decodeAccessToken
from app.services import category_service
from app.schemas.user_schema import User
from app.schemas.category_schema import Category
from app.schemas.category_schema_update import CategoryUpdate


router = APIRouter()

@router.get("/greeting")
def greeting():
    return {"message": "Hello world category"}

@router.post("/create-category")
async def createCategory(category: Category, currentUser = Depends(decodeAccessToken)):
    return await category_service.createCategory(category, currentUser)

@router.get("/get-categories")
async def getCategories(currentUser = Depends(decodeAccessToken)):
    return await category_service.getCategories(currentUser)

@router.get("/get-categories-over-budget")
async def categoriesOverBudget(currentUser = Depends(decodeAccessToken)):
    return await category_service.categoriesOverBudget(currentUser)

@router.put("/update-category/{idCategory}")
async def categoryUpdate(updateCategory: CategoryUpdate, idCategory: str, currentUser = Depends(decodeAccessToken)):
    return await category_service.updateCategoryByUser(currentUser, updateCategory, idCategory)