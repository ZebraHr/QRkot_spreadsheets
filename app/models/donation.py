from sqlalchemy import Column, ForeignKey, Text, Integer

from app.models.abstract_base import AbstractBase


class Donation(AbstractBase):
    """Модель для пожертвований."""
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
