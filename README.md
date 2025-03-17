# LibraryAPI

## Технологии

Проект использует следующие технологии и библиотеки:

- [Python](https://www.python.org/) — основной язык программирования.
- [FastAPI](https://fastapi.tiangolo.com/) — асинхронный web-фреймворк для API.
- [PostgreSQL](https://www.postgresql.org/) — реляционная база данных.
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM для работы с базой данных.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) — инструмент для миграций базы данных.
- [Pydantic](https://docs.pydantic.dev/latest/) — валидация данных и управление настройками.
- [Redis](https://redis.io/) — кеширование и брокер сообщений.
- [aioredis](https://github.com/aio-libs/aioredis-py) — асинхронный клиент для Redis.
- [asyncpg](https://github.com/MagicStack/asyncpg) — асинхронный драйвер для PostgreSQL.
- [Uvicorn](https://www.uvicorn.org/) — ASGI-сервер для FastAPI.
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/) — работа с JWT-токенами.
- [Passlib](https://passlib.readthedocs.io/en/stable/) — хеширование паролей.
- [pytest](https://docs.pytest.org/en/latest/) — тестирование.
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) — тестирование асинхронного кода.

## Сборка и запуск через Docker

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/Randazzz/LibraryAPI
   cd ваш-репозиторий
   ```
2. Создайте файлы .env.* на основе примера .env.example и настройте переменные окружения

3. Соберите Docker-образы и запустите проект:

   ```bash
   docker-compose --env-file .env.dev up --build
   ```
   или
   ```bash
   docker-compose --env-file .env.prod up --build
   ```

4. Если вы хотите запустить контейнеры в фоновом режиме, используйте флаг -d:

   ```bash
   docker-compose --env-file .env.dev up --build -d
   ```
После запуска проекта вы можете перейти по адресу http://127.0.0.1:8000/docs
или http://127.0.0.1:8000/redoc, чтобы получить доступ к интерактивной документации API.

## Структура
<details>
  <summary><strong>Структура проекта</strong></summary>

```markdown
Library/
└── src/
│  ├── api/
│  │   └── v1/
│  │   │  ├── __init__.py
│  │   │  ├── auth.py
│  │   │  ├── author.py
│  │   │  ├── book.py
│  │   │  ├── genre.py
│  │   │  └── user.py
│  │   └── __init__.py
│  ├── core/
│  │   └── exceptions/
│  │   ├── __init__.py
│  │   ├── auth.py
│  │   ├── config.py
│  │   ├── dependencies.py
│  │   ├── logging.py
│  │   ├── security.py
│  │   └── validations.py
│  ├── db/
│  │   ├── models/
│  │   │   ├── __init__.py
│  │   │   ├── associations.py
│  │   │   ├── books.py
│  │   │   ├── users.py
│  │   │   └── utils.py
│  │   ├── repositories/
│  │   │   ├── __init__.py
│  │   │  ├── author.py
│  │   │  ├── book.py
│  │   │  ├── genre.py
│  │   │   └── user.py
│  │   ├── __init__.py
│  │   ├── base.py
│  │   └── database.py
│  ├── migrations/
│  ├── schemas/
│  │   ├── __init__.py
│  │   ├── auth.py
│  │   ├── author.py
│  │   ├── book.py
│  │   ├── common.py
│  │   ├── genre.py
│  │   └── user.py
│  ├── services/
│  │   ├── __init__.py
│  │   ├── auth.py
│  │   ├── author.py
│  │   ├── book.py
│  │   ├── genre.py
│  │   └── user.py
│  ├── __init__.py
│  └── main.py
├── tests/
├── .dockerignore
├── .env.dev
├── .env.example
├── .env.prod
├── .env.test
├── .gitignore
├── .alembic.ini
├── .docker-compose.yml
├── Dockerfile
├── logging.log
├── entrypoint.sh
├── pyproject.toml
├── README.md
└── requirements.txt
```
</details>