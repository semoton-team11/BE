# 커리큘럼 계산기
from fastapi import APIRouter, Depends
from app.schemas.curriculum import (CoursesResponse, CurriculumRequest, CurriculumResponse, GraduationResponse, CurriculumUpdateRequest)
from app.services.curriculum_service import (fetch_courses, fetch_curriculum, save_curriculum, change_status, delete_curriculum, calculate_graduation, fetch_all_courses_by_dept, fetch_graduation_requirements)
from app.dependencies.database import get_supabase
from app.dependencies.auth import get_current_user
from app.utils.responses import success_response, error_response
from typing import List                                 
router = APIRouter(prefix="/curriculum", tags=["Curriculum"])

# GET    /curriculum/{user_id}                  -> 나의 이수 과목 조회
# POST   /curriculum/{user_id}                  -> 나의 이수 과목 추가
# DELETE /curriculum/{user_id}/{course_id}      -> 나의 이수 과목 삭제
# PATCH  /curriculum/{user_id}/{curriculum_id}  -> 나의 이수 여부 변경
# GET    /curriculum/{user_id}/graduation       -> 졸업 요건 계산

# 학과별 전체 과목(카탈로그) 조회
@router.get("/courses")
async def get_catalog_courses(
    supabase=Depends(get_supabase),
    user=Depends(get_current_user)
):
    metadata = user.get("user_metadata", {})
    dept = metadata.get("department")
    
    if not dept:
        return error_response(message="사용자의 학과 정보가 등록되지 않았습니다.", status_code=400)

    data = fetch_all_courses_by_dept(dept, supabase)
        
    return success_response(
        data = data, 
        message=f"[{dept}] 카탈로그 조회 성공"
    )

# 졸업 요건 가져오기
@router.get("/requirements")
async def get_requirements(user=Depends(get_current_user)):
    dept = user.get("user_metadata", {}).get("department")
    data = fetch_graduation_requirements(dept)
    if not data:
        return error_response("요건 정보 없음", 404)
    return success_response(data)

# 나의 이수 과목 조회
@router.get("/{user_id}")
async def get_curriculum_by_user(
    user_id: str,
    supabase=Depends(get_supabase),
    user=Depends(get_current_user)
):
    data = fetch_curriculum(user_id, supabase)
    return success_response(data=data, message="이수 과목 조회 성공")

# 나의 이수 과목 추가
@router.post("/{user_id}")
async def create_curriculum(
    user_id: str,
    request: CurriculumRequest,
    supabase=Depends(get_supabase),
    user=Depends(get_current_user)
):
    data = save_curriculum(user_id, request, supabase)
    return success_response(data=data, message="과목 추가 성공")

# 나의 이수 여부 변경
@router.patch("/{user_id}/{curriculum_id}")
async def update_status(
    user_id: str,
    curriculum_id: str,
    request: CurriculumUpdateRequest,
    supabase=Depends(get_supabase),
    user=Depends(get_current_user)
):
    data = change_status(user_id, curriculum_id, request, supabase)
    if isinstance(data, dict) and "error" in data:
        return error_response(message=data["error"], code="NOT_FOUND")
    return success_response(data=data, message="이수여부 수정 성공")

# 나의 이수 과목 삭제
@router.delete("/{user_id}/{curriculum_id}")
async def delete_curriculum_by_user(
    user_id: str,
    curriculum_id: str,
    supabase=Depends(get_supabase),
    user=Depends(get_current_user)
):
    data = delete_curriculum(user_id, curriculum_id, supabase)
    return success_response(data=data, message="과목 삭제 성공")

# 졸업 요건 계산
@router.get("/{user_id}/graduation")
async def get_graduation_status(user_id: str, supabase=Depends(get_supabase), user=Depends(get_current_user)):
    data = calculate_graduation(user_id, supabase)
    if isinstance(data, dict) and "error" in data:
        return error_response(message=data["error"], code="NOT_SUPPORTED")
    print("졸업 요건 계산 성공")
    return success_response(data=data, message="졸업 요건 조회 성공")

