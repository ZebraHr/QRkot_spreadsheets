from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(self,
                                     project_name: str,
                                     session: AsyncSession,
                                     ) -> Optional[int]:
        """Получение id проекта по названию."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )

        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        """Получение списка закрытых проектов по количеству времени на закрытие."""
        db_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(CharityProject.close_date - CharityProject.create_date)
        )
        return db_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
