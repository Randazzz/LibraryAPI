# LibraryAPI

## Установка и запуск

### Сборка и запуск через Docker

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/ваш-username/ваш-репозиторий.git
   cd ваш-репозиторий
   ```
2. Создайте файл .env.dev на основе примера .env.example и настройте переменные окружения


3. Соберите Docker-образы:

   ```bash
   docker-compose --env-file .env.dev build
   ```
4. Запустите проект:

   ```bash
   docker-compose --env-file .env.dev up
   ```
5. Если вы хотите запустить контейнеры в фоновом режиме, используйте флаг -d:

   ```bash
   docker-compose --env-file .env.dev up -d
   ```
После запуска проекта вы можете перейти по адресу http://127.0.0.1:8000/docs
или http://127.0.0.1:8000/redoc, чтобы получить доступ к интерактивной документации API.
