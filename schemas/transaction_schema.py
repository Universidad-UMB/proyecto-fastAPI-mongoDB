from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class Transaction(BaseModel):
    amount: float
    type: Literal["ingreso", "gasto"]
    category: str
    description: str