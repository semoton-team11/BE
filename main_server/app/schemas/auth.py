from pydantic import BaseModel


class UserSignup(BaseModel):
    email: str
    password: str
    department: str
    student_id: int


class UserLogin(BaseModel):
    email: str
    password: str
