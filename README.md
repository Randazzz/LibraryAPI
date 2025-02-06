# LibraryAPI

## Установка и запуск

### Сборка и запуск через Docker

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/Randazzz/LibraryAPI
   cd ваш-репозиторий
   ```
2. Создайте файл .env.dev на основе примера .env.example и настройте переменные окружения


3. Соберите Docker-образы и запустите проект:

   ```bash
   docker-compose --env-file .env.dev up --build
   ```

4. Если вы хотите запустить контейнеры в фоновом режиме, используйте флаг -d:

   ```bash
   docker-compose --env-file .env.dev up --build -d
   ```
После запуска проекта вы можете перейти по адресу http://127.0.0.1:8000/docs
или http://127.0.0.1:8000/redoc, чтобы получить доступ к интерактивной документации API.
