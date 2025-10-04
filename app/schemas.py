from pydantic import BaseModel
from datetime import datetime

class CurrencyRateCreate(BaseModel):
    base_currency: str
    target_currency: str
    rate: float

class CurrencyRateResponse(BaseModel):
    id: int
    base_currency: str
    target_currency: str
    rate: float
    timestamp: datetime

    class Config:
        orm_mode = True
