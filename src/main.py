from datetime import timedelta

import jwt
from fastapi import FastAPI, Depends, HTTPException
from schemas import UserSchema, UserSalary
from auth import create_access_token, get_password_hash, verify_password, oauth2_scheme, SECRET_KEY, ALGORITHM

users = {
    'John': UserSalary(
        username='John',
        password=get_password_hash('1234'),
        salary=30000,
        next_raise_date='2025-12-12'
    ),
    'Alice': UserSalary(
        username='Alice',
        password=get_password_hash('qwerty'),
        salary=63500,
        next_raise_date='2026-01-25'
    ),
}

app = FastAPI()


@app.post('/login')
async def authenticate_user(data: UserSchema):
    username = data.username
    password = data.password
    user = users.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail='Не удалось войти')
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail='Неверный пароль')
    token = create_access_token({'sub': user.username}, expires_delta=timedelta(minutes=30))
    return {'token': token, 'token_type': 'Bearer'}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=400, detail=f'Неверное имя пользователя')

    user = users.get(username)
    if user is None:
        raise HTTPException(status_code=400, detail=f'Не существует такого пользователя')
    return user


@app.get('/salary_info')
async def get_salary_info(user: UserSalary = Depends(get_current_user)):
    return {
        'username': user.username,
        'salary': user.salary,
        'next_raise_date': user.next_raise_date
    }

