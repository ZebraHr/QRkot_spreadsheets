# Приложение для Благотворительного фонда поддержки котиков QRKot. 

### Описание
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции. 

### Возможности
- Создание благотворительных целевых проектов (администратором сайта)
- Создание пожертвований (любым пользователем)
- Pабота с api
- Формирование отчета в гугл-таблице с проектами, отсортированными по скорости сбора средств

### Технологии
- Python 3.9
- Фреймворк FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Asyncio
- Google Cloud Platform
- Google Sheets Api
- Googla Drive Api

### Запуск проекта
- Клонируйте репозитоий
```
git clone https://github.com/ZebraHr/QRkot_spreadsheets
```
- Установите и активируйте виртуальное окружение
```
python3 -m venv venv
source venv/Scripts/activate
```
```
python3 -m pip install --upgrade pip
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
-  в корневой папке проекта создайте файл .env со следующим содержимым:
```
APP_TITLE=<Ваш вариант названия проекта>
PROJECT_DESCRIPTION=<Ваш вариант описания проекта>
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=<Ваш вариант серкретного ключа>
FIRST_SUPERUSER_EMAIL=<e-mail для автоматического создания суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль для автоматического создания суперюзера>

Данные, получаемые после настройки Google Cloud:
EMAIL=<ваш e-mail гугл-аккаунта>
TYPE=service_account
PROJECT_ID=<идентификатор>
PRIVATE_KEY_ID=<id приватного ключа>
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----<приватный ключ>-----END PRIVATE KEY-----\n
CLIENT_EMAIL=<email сервисного аккаунта>
CLIENT_ID=<id сервисного аккаунта>
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https:<ваша ссылка на местоположение общедоступных сертификатов (X.509) публичных ключей для сервисных аккаунтов Google в формате JSON Web Key (JWK), которые используются для аутентификации>
UNIVERSE_DOMAIN=googleapis.com
```
- создайте базу данных, применив миграции (из корневой папки проекта)
```
alembic upgrade head
```

- запустите проект локально (из корневой папки проекта)
```
uvicorn app.main:app --reload
```
- описание эндпоинтов и возможностей доступно по этим ссылкам
```
Swagger: http://127.0.0.1:8000/docs
или
Redoc: http://127.0.0.1:8000/redoc
```
### Примеры команд для работы с api
Пример POST-запроса для создания благотворительного проекта:
```
POST ... http://127.0.0.1:8000/charity_project/
{
"name": "string",
"description": "string",
"full_amount": 0
}
```
Пример ответа:
```
{
"name": "string",
"description": "string",
"full_amount": 0,
"id": 0,
"invested_amount": 0,
"fully_invested": true,
"create_date": "2019-08-24T14:15:22Z",
"close_date": "2019-08-24T14:15:22Z"
}
```
Пример POST-запроса для совершения пожертвования:
```
POST ... http://127.0.0.1:8000/donation/
{
"full_amount": 0,
"comment": "string"
}
```
Пример ответа:
```
{
"full_amount": 0,
"comment": "string",
"id": 0,
"create_date": "2019-08-24T14:15:22Z"
}
```
Пример GET-запроса для получения списка всех пожертвований:
```
GET ... http://127.0.0.1:8000/donation/
```
Пример ответа:
```
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2019-08-24T14:15:22Z",
    "user_id": "string",
    "invested_amount": 0,
    "fully_invested": true,
    "close_date": "2019-08-24T14:15:22Z"
  }
]
```
Пример POST-запроса для формирования отчета:
```
POST ... http://127.0.0.1:8000/google/
```
На ваш e-mail гугл-аккаунта придет ссылка на сформирвоанный отчет
### Автор
Анна Победоносцева.
Студент Яндекс Практикума "Python-разаботчик плюс".
г. Москва.
GitHub: https://github.com/ZebraHr
