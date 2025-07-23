from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from schemas import UserSchema

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/users')
async def get_users(db: Session = Depends(get_db)):
    return db.execute(select(User)).scalars().all()


@app.post('/users')
async def add_user(data: UserSchema, db: Session = Depends(get_db)):
    name = data.name
    email = data.email
    try:
        db.execute(insert(User).values(name=name, email=email))
        db.commit()
        return 'Пользователь успешно добавлен'
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail='Не удалось добавить пользователя')
