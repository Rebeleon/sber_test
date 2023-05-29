from datetime import datetime
from pydantic import BaseModel, validator


class DepositRequest(BaseModel):
    date: str
    periods: int
    amount: int
    rate: float

    @validator('date')
    def check_date(cls, v):
        try:
            datetime.strptime(v, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Date must be in DD.MM.YYYY format')
        return v

    @validator('periods')
    def check_periods(cls, v):
        if not (1 <= v <= 60):
            raise ValueError('Periods must be between 1 and 60')
        return v

    @validator('amount')
    def check_amount(cls, v):
        if not (10000 <= v <= 3000000):
            raise ValueError('Amount must be between 10000 and 3000000')
        return v

    @validator('rate')
    def check_rate(cls, v):
        if not (1 <= v <= 8):
            raise ValueError('Rate must be between 1 and 8')
        return v
