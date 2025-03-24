# Flask Blog

## Сборка приложения
1. Клонировать репозиторий и перейти в корень приложения
2. Запустить сборку образа приложения:  
`docker build -t flask_blog .`  
3. Запустить контейнеры БД и приложения (веб-сервер)  
`docker compose up -d`

## REST API
Swagger UI http://localhost:5000/openapi/swagger  

## Frontend
URL http://localhost:5000  
Логин: username  
Пароль: password

## Test
Запуск pytest  
`coverage run -m pytest`  