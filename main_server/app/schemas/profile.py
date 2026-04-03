from pydantic import BaseModel
from typing import Optional

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    student_id: Optional[str] = None
    is_graduated: Optional[bool] = None
    grade: Optional[int] = None

class ScrapbookCreate(BaseModel):
    target_user_id: str  