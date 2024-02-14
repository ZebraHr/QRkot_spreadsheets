from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean

from app.core.db import Base


class AbstractBase(Base):
    """Абстрактная модель."""
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)
