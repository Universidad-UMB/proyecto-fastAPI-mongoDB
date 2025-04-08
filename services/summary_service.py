from app.db.database import collectionItem
from app.schemas.user_schema import User


async def monthlySummary(currentUser: User):
    spents = await collectionItem.categories.find({"user_id": currentUser["_id"]}, { "spent": 1, "_id": 0 }).to_list(length=None)
    incomes = await collectionItem.categories.find({"user_id": currentUser["_id"]},{ "income": 1, "_id": 0 }).to_list(length=None)
   
    
    totalIncomes = sum(income["income"] for income in incomes)
    totalSpents = sum(spent["spent"] for spent in spents)

    
    generalBalance = totalIncomes - totalSpents
    
    return {"income total": totalIncomes,
            "spent total": totalSpents,
            "general balance": generalBalance}
    