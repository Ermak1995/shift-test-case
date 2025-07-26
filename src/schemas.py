from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    hashed_password: str
    salary: float
    next_raise_date: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserSalarySchema(BaseModel):
    username: str
    salary: float
    next_raise_date: str
