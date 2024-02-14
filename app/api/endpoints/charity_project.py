from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.crud.charity_project import charity_project_crud
from app.api.validators import (check_charity_project_exists, check_name_duplicate,
                                check_charity_project_closed,
                                check_charity_project_invested_sum,
                                check_charity_project_already_invested)
from app.core.user import current_superuser
from app.services.investing import investing
from app.models import Donation


router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],
             )
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Создает благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)

    new_project = await charity_project_crud.create(charity_project, session)
    return await investing(new_project, Donation, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Удаляет проект.
    Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    check_charity_project_already_invested(charity_project)
    check_charity_project_closed(charity_project)
    return await charity_project_crud.remove(
        charity_project, session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать, также нельзя установить
    требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    check_charity_project_closed(charity_project)

    if obj_in.full_amount is not None:
        check_charity_project_invested_sum(charity_project, obj_in.full_amount)
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )
