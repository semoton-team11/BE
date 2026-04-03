from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional

class UserSignup(BaseModel):
    email: str
    password: str
    name: str
    department: str
    student_id: str
    is_graduated: bool = False
    grade: Optional[int] = None
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class UserLogin(BaseModel):
    email: str
    password: str