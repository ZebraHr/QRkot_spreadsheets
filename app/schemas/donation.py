from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationUser(DonationCreate):
    create_date: datetime
    id: int

    class Config:
        orm_mode = True


class DonationDB(DonationUser):
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
