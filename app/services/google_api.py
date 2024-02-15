from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import (
    settings, DATE_FORMAT, ROW_COUNT, COLUMN_COUNT, SHEET_ID
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создание гугл-таблицы."""
    now_date_time = datetime.now().strftime(DATE_FORMAT)

    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': SHEET_ID,
                    'title': 'Лист1',
                    'gridProperties': {
                        'rowCount': ROW_COUNT,
                        'columnCount': COLUMN_COUNT
                    }
                }
            }
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Выдача прав личному аккаунту."""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Обновление данных в таблице."""
    now_date_time = datetime.now().strftime(DATE_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in charity_projects:
        new_row = [
            project.name,
            str(project.close_date - project.create_date),
            project.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_services.as_service_account(  # noqa
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )