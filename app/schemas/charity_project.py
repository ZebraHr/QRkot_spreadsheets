from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, validator, Extra


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    create_date: datetime
    close_date: Optional[datetime]
    fully_invested: bool

    class Config:
        orm_mode = True
