from sqlalchemy import Column, String, Text

from app.models.abstract_base import AbstractBase


class CharityProject(AbstractBase):
    """Модель для проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
