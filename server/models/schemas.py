from pydantic import BaseModel

class UserAuth(BaseModel):
  email: str
  password: str
  department: str
  student_id: int

class UserLogin(BaseModel):
    email: str
    password: str