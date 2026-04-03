from pydantic import BaseModel
from typing import Optional


class SeniorBase(BaseModel):
    """선배 공통 필드"""
    id: str
    user_id: str
    name: Optional[str]
    department: Optional[str]
    graduated_year: Optional[int] = None
    bio: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    is_available: bool
    skills: list


class SeniorSummary(SeniorBase):
    """선배 목록 조회 응답"""
    pass


class CurriculumGridItem(BaseModel):
    """학업 여정 그리드 항목"""
    year_level: int
    semester_type: int
    course_name: str


class MentoringSlot(BaseModel):
    """멘토링 가능 시간 슬롯"""
    id: str
    available_date: str
    start_time: str
    end_time: str


class SeniorDetail(SeniorBase):
    """선배 상세 프로필 응답"""
    curriculum_grid: list[CurriculumGridItem] = []
    mentoring_slots: list[MentoringSlot] = []
