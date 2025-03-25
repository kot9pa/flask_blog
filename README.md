# Flask Blog

## Сборка приложения
1. Переименовать `.env.example` в `.env` (изменить значения, по необходимости)
2. Запустить сборку образа приложения:  
`docker build -t flask_blog .`  
3. Запустить docker-контейнеры   
`docker compose up -d`

## REST API
Swagger UI   
http://localhost:5000/openapi/swagger  

## Frontend
URL http://localhost:5000  
Логин: username  
Пароль: password

## Tests
Запуск pytest в контейнере docker  
`docker exec flask_blog coverage run -m pytest > result.log`  

Результаты тестирования будут в файле result.log