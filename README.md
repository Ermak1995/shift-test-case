# Тестовое задание SHIFT

## Запуск сервиса

**1. Клонирование репозитория**
```bash
  git clone https://github.com/Ermak1995/shift-test-case.git
```

**2. Сборка Docker-образа**
```bash 
  docker build -t salary-app .
```

**3. Запуск Docker-контейнера**
```bash
  docker run -d -p 8000:8000 -e SECRET_KEY="ваше_секретное_слово" --name salary-service salary-app
```    
## Взаимодействие с API

**1. Аутентификация пользователя (`POST /login`)**

**Пример с `curl`:**
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{ "username": "John", "password": "1234" }'
``` 

**Успешный ответ:**

```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```


**2. Получение информации о зарплате (`GET /salary_info`)**

**Пример с `curl` (замените `<ваш_токен_доступа>` на полученный токен):**
```bash
curl -X GET "http://localhost:8000/salary_info" \
     -H "Authorization: Bearer <ваш_токен_доступа>" 
```

## Тестирование
Для проверки тестов в запущенном контейнере выполните команду
```bash
docker exec <имя_контейнера> pytest
```