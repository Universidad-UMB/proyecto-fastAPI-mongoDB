from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Category(BaseModel):
    name: str
    budget: float
    income: float
  