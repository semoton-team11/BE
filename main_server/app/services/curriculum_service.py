from app.schemas.curriculum import (CoursesResponse, CurriculumRequest, CurriculumResponse, CourseInfo, CurriculumUpdateRequest, CategoryCredit, GraduationResponse)

# 졸업 요건
GRADUATION_REQUIREMENTS = {
    # 소프트웨어융합대학
    "컴퓨터공학과": {
        "전공필수": 39,
        "전공선택": 30,
        "전공기초": 12,
        "교양": 49,
        "total": 130,
    },
    "소프트웨어융합학과": {
        "전공필수": 37,
        "전공선택": 36,
        "전공기초": 15,
        "교양": 42,
        "total": 130,
    },
    "소융": {
        "전공필수": 37,
        "전공선택": 36,
        "전공기초": 15,
        "교양": 42,
        "total": 130,
    },
    "인공지능학과": {
        "전공필수": 42,
        "전공선택": 27,
        "전공기초": 12,
        "교양": 49,
        "total": 130,
    },
    # 예술 디자인 대학
    "산업디자인학과": {
        "전공기초": 18,
        "전공선택": 28,
        "전공필수": 21,
        "교양": 53,
        "total": 120,
    },
    "시각디자인학과": {
        "전공기초": 6,
        "전공선택": 61,
        "전공필수": 0,
        "교양": 53,
        "total": 120,
    },
    "환경조경디자인학과": {
        "전공기초": 9,
        "전공선택": 46,
        "전공필수": 12,
        "교양": 53,
        "total": 120,
    },
    "디지털콘텐츠학과": {
        "전공기초": 12,
        "전공선택": 55,
        "전공필수": 0,
        "교양": 53,
        "total": 120,
    },
    "의류디자인학과": {
        "전공기초": 12,
        "전공선택": 46,
        "전공필수": 9,
        "교양": 53,
        "total": 120,
    },
    "도예학과": {
        "전공기초": 15,
        "전공선택": 43,
        "전공필수": 9,
        "교양": 53,
        "total": 120,
    },
    "연극영화학과": {
        "전공기초": 10,
        "전공선택": 42,
        "전공필수": 13,
        "교양": 55,
        "total": 120,
    },
    "포스트모던음악학과": {
        "전공기초": 12,
        "전공선택": 43,
        "전공필수": 12,
        "교양": 53,
        "total": 120,
    },
}

# 학과 조회
def fetch_departments(supabase):
    result = supabase.table("courses_master").select("dept_name").execute()
    seen = set()
    departments = []
    for item in result.data:
        dept = item["dept_name"]
        if dept and dept not in seen:
            seen.add(dept)
            departments.append(dept)
    return departments

# 학과 과목 조회
def fetch_courses(dept_name: str, supabase):
    result = supabase.table("courses_master").select("*").eq("dept_name", dept_name).execute()
    return result.data

# 나의 이수 과목 조회
def fetch_curriculum(user_id: str, supabase):
    result = supabase.table("curriculums").select("id, course_id, semester, grade, completed, courses_master(course_name, course_type, credits, college_name, dept_name)").eq("user_id", user_id).execute()
    return result.data

# 나의 이수 과목 추가
def save_curriculum(user_id: str, request: CurriculumRequest, supabase):
    result = supabase.table("curriculums").insert({
        "user_id": user_id,
        "course_id": request.course_id,
        "semester": request.semester,
        "grade": request.grade,
        "completed": request.completed,
    }).execute()
    saved_id = result.data[0]["id"]
    full_result = supabase.table("curriculums").select("id, course_id, semester, grade, completed, courses_master(course_name, course_type, credits, college_name, dept_name)") \
        .eq("id", saved_id).execute()
    return full_result.data[0]

# 나의 이수 여부 변경
def change_status(user_id: str, curriculum_id: str, request, supabase):
    supabase.table("curriculums").update({"completed": request.completed, "grade": request.grade}).eq("id", curriculum_id).eq("user_id", user_id).execute()
    result = supabase.table("curriculums") \
        .select("id, course_id, semester, grade, completed, courses_master(course_name, course_type, credits, college_name, dept_name)") \
        .eq("id", curriculum_id) \
        .execute()
    return result.data[0]

# 나의 이수 과목 삭제
def delete_curriculum(user_id: str, curriculum_id: str, supabase):
    supabase.table("curriculums").delete().eq("id", curriculum_id).eq("user_id", user_id).execute()
    return {"message": "삭제 완료"}

# 졸업 요건 계산
def calculate_graduation(user_id: str, supabase):
    user = supabase.table("users").select("department").eq("id", user_id).execute()
    department = user.data[0]["department"]     # 유저 학과 조회
    requirements = GRADUATION_REQUIREMENTS.get(department) 
    
    # 이수 완료한 과목 조회
    result = supabase.table("curriculums").select("*, courses_master(credits, course_type)").eq("user_id", user_id).eq("completed", True).execute()
    
    # 전공 카테고리별 이수 학점 계산
    completed_by_category = {
        "전공필수": 0,
        "전공선택": 0,
        "전공기초": 0,
    }

    for item in result.data:
        course = item.get("courses_master")
        if course:
            category = course.get("course_type")
            credits = course.get("credits", 0)
            if category in completed_by_category:
                completed_by_category[category] += credits

    # 전공 카테고리별 응답
    categories = []
    total_completed = 0

    for category in ["전공필수", "전공선택", "전공기초"]:
        completed = completed_by_category[category]
        required = requirements[category]
        remaining = max(0, required - completed)
        total_completed += completed

        categories.append(CategoryCredit(
            category=category,
            completed=completed,
            required=required,
            remaining=remaining,
        ))
        
    # 총합 응답
    total_required = requirements["total"]
    total_remaining = max(0, total_required - total_completed)

    return GraduationResponse(
        department,
        categories=categories,
        total_completed=total_completed,
        total_required=total_required,
        total_remaining=total_remaining,
    )
  
  # 특정 학과에 개설된 전체 과목 리스트(카탈로그) 조회
def fetch_all_courses_by_dept(dept: str, supabase):
    conditions = []

    if dept in ["소프트웨어융합학과", "소융"]:
      conditions.append("college_name.eq.소프트웨어융합대학")
      conditions.extend([
          "course_id.ilike.AMTH%", "course_id.ilike.IE%", "course_id.ilike.MEC%"
      ])
      conditions.extend([
          "course_name.eq.물리학및실험1", "course_name.eq.로봇제어공학", 
          "course_name.eq.세계신화읽기", "course_name.eq.테크놀로지와디지털콘텐츠"
      ])
    elif dept in ["컴퓨터공학과", "컴공"]:
      conditions.append("college_name.eq.소프트웨어융합대학")
      conditions.append("course_id.ilike.AMTH%")
      conditions.extend([
          "course_name.eq.확률및랜덤변수", "course_name.eq.논리회로", "course_name.eq.신호와시스템"
      ])
    elif dept in ["인공지능학과", "인지"]:
      conditions.append("college_name.eq.소프트웨어융합대학")
      conditions.append("course_id.ilike.AMTH%")
      conditions.append("course_name.eq.확률및랜덤변수")
    
    elif dept in ["산업디자인학과", "산디"]:
        conditions.append("course_id.ilike.FD%")
        conditions.append("dept_name.eq.산업디자인학과")
    if not conditions:
        return []
    
    query = ",".join(conditions)

    response = supabase.table("courses_master") \
        .select("*") \
        .or_(query) \
        .order("course_name") \
        .execute()
    
    return response.data


# 졸업 요건 가져오기
def fetch_graduation_requirements(dept: str):
    """
    학과명에 해당하는 졸업 기준 학점만 반환
    """
    # 전공명 매핑 (소융 -> 소프트웨어융합학과 등)
    dept_map = {
        "소융": "소프트웨어융합학과",
        "컴공": "컴퓨터공학과",
        "인지": "인공지능학과",
        "산디": "산업디자인학과"
    }
    
    actual_dept = dept_map.get(dept, dept)
    requirements = GRADUATION_REQUIREMENTS.get(actual_dept)

    if not requirements:
        return None

    return {
        "dept_name": actual_dept,
        "required": requirements.get("전공필수", 0),
        "elective": requirements.get("전공선택", 0),
        "basic": requirements.get("전공기초", 0),
        "liberal": requirements.get("교양", 0),
        "total": requirements.get("total", 120)
    }