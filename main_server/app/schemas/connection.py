from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class ConnectionCreate(BaseModel):
    senior_id: UUID
    message: str = Field(max_length=500)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("message must not be blank")
        return value
