from pydantic import BaseModel
from typing import Optional, List

# 학과 조회 응답
class CoursesResponse(BaseModel):
    course_id: str
    college_name: str
    dept_name: Optional[str] = None
    course_name: str
    course_type: str
    credits: Optional[int] = None

# 이수 과목 저장
class CurriculumRequest(BaseModel):
    course_id: str
    semester: str
    grade: Optional[str] = None
    completed: bool = False

# 이수 과목 조회
class CourseInfo(BaseModel):
    course_name: str
    course_type: str
    credits: int
    college_name: str
    dept_name: str

class CurriculumResponse(BaseModel):
    id: str
    course_id: str
    semester: str
    grade: Optional[str] = None
    completed: bool = False
    courses_master: CourseInfo
    
# 이수 여부 수정
class CurriculumUpdateRequest(BaseModel):
    completed: bool
    grade: Optional[str] = None
    
# 카테고리별 학점
class CategoryCredit(BaseModel):
    category: str       # 전공필수 / 전공선택 / 전공기초
    completed: int      # 이수한 학점
    required: int       # 필요한 학점
    remaining: int      # 남은 학점

# 졸업 요건 계산
class GraduationResponse(BaseModel):
    categories: List[CategoryCredit] # [ {category: "전공필수", completed: 6, required: 21, remaining: 15} ]
    total_completed: int    # 전체 이수 학점
    total_required: int     # 전체 필요 학점
    total_remaining: int    # 전체 남은 학점