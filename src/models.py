from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    login: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String())
