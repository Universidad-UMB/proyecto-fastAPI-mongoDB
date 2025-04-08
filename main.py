from fastapi import FastAPI
from app.routes import item_router
from app.routes import auth_router
from app.routes import transaction_router
from app.routes import category_router
from app.routes import summary_router

app = FastAPI()

app.include_router(item_router, prefix="/items")
app.include_router(auth_router, prefix="/auth")
app.include_router(transaction_router, prefix="/transaction")
app.include_router(category_router, prefix="/category")
app.include_router(summary_router, prefix="/summary")