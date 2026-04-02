from uuid import UUID
from datetime import date, time
from pydantic import BaseModel, Field, model_validator
from typing import Optional


class ScheduleCreate(BaseModel):
    """약속 생성 요청"""
    connection_id: UUID = Field(..., description="연결 ID")
    available_date: date = Field(..., description="약속 날짜")
    start_time: time = Field(..., description="시작 시간")
    end_time: time = Field(..., description="종료 시간")

    @model_validator(mode="after")
    def validate_schedule(self):
        if self.available_date < date.today():
            raise ValueError("과거 날짜에는 약속을 잡을 수 없습니다.")
        if self.start_time >= self.end_time:
            raise ValueError("end_time은 start_time보다 뒤여야 합니다.")
        return self


class ScheduleResponse(BaseModel):
    """약속 응답"""
    id: str
    mentor_id: str
    mentee_id: str
    available_date: str
    start_time: str
    end_time: str
    is_reserved: bool
    created_at: Optional[str] = None
