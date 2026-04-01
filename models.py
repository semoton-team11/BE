from pydantic import BaseModel
from typing import Optional

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    major: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class ScrapbookCreate(BaseModel):
    target_user_id: str  