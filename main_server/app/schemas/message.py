from pydantic import BaseModel, Field, field_validator


class MessageCreate(BaseModel):
    """메시지 전송 요청"""
    content: str = Field(..., max_length=2000, description="메시지 내용")

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("content must not be blank")
        return value
