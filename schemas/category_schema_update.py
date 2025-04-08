from pydantic import BaseModel
from typing import Optional

class CategoryUpdate(BaseModel):
    name: Optional[str]=None
    budget: Optional[float]=None
    income: Optional[float]=None