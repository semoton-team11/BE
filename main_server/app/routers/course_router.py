# 과목 데이터 (팀원1)
from fastapi import APIRouter, Depends
from app.schemas.curriculum import (CoursesResponse)
from app.services.curriculum_service import (fetch_departments, fetch_courses)
from app.dependencies.database import get_supabase
from app.dependencies.auth import get_current_user
from app.utils.responses import success_response, error_response
from typing import List

router = APIRouter(prefix="/courses", tags=["Course"])

# GET    /courses/departments              -> 학과 조회
# GET    /courses/{dept_name}              -> 학과 과목 조회

#학과 조회
@router.get("/departments")
async def get_departments(supabase=Depends(get_supabase), user=Depends(get_current_user)):
    data = fetch_departments(supabase)
    return success_response(data=data, message="학과 목록 조회 성공")


# 학과 과목 조회
@router.get("/departments/{dept_name}", response_model=List[CoursesResponse])
async def get_courses(dept_name: str, supabase=Depends(get_supabase), user=Depends(get_current_user)):
    data = fetch_courses(dept_name, supabase)
    return success_response(data=data, message="과목 목록 조회 성공")