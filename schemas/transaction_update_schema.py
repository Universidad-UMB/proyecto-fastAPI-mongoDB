from pydantic import BaseModel
from typing import Optional, Literal

class UpdateTransaction(BaseModel):
    amount: Optional[float]
    type: Optional[Literal["ingreso", "gasto"]]
    category: Optional[str]
    description: Optional[str]