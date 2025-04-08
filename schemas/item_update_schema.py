from pydantic import BaseModel
from typing import Optional

class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]