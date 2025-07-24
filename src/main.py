from datetime import timedelta

import jwt
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from schemas import UserSchema, UserSalary
from auth import create_access_token, get_password_hash, verify_password, oauth2_scheme, SECRET_KEY, ALGORITHM

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/register')
async def registrate_user(data: UserSalary, db: Session = Depends(get_db)):
    data.password = get_password_hash(data.password)
    new_user = User(**data.dict())
    try:
        db.add(new_user)
        db.commit()
        return 'Регистрация успешна'
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=401, detail=f'Ошибка: {e}')


@app.post('/login')
async def authenticate_user(data: UserSchema, db: Session = Depends(get_db)):
    username = data.username
    password = data.password
    user = db.execute(select(User).where(User.username==username)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail='Не удалось войти')
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail='Неверный пароль')
    token = create_access_token({'sub': user.username}, expires_delta=timedelta(minutes=30))
    return {'token': token, 'token_type': 'Bearer'}


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=400, detail=f'Неверное имя пользователя')

    user = db.execute(select(User).where(User.username==username)).scalar_one_or_none()
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
