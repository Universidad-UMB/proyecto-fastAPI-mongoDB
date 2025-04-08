from pydantic import BaseModel

class Summary(BaseModel):
    summaryIncome: float
    summarySpent: float
    summaryBalance: float