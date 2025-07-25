from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserSalary(UserSchema):
    salary: float
    next_raise_date: str