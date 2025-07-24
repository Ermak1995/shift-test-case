from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String())
    salary: Mapped[float] = mapped_column()
    next_raise_date: Mapped[date] = mapped_column(Date())
