from datetime import date
from fastapi import HTTPException
from postgrest.exceptions import APIError
from app.utils.responses import success_response


async def list_seniors(department: str | None, supabase):
    try:
        query = (
            supabase.table("senior_profiles")
            .select("id, user_id, bio, job_title, company, graduated_year, is_available, skills, users!inner(name, department), timetable")
        )

        if department:
            query = query.eq("users.department", department)

        response = query.execute()
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "선배 목록 조회에 실패했습니다.", "code": "FETCH_FAILED"})

    seniors = []
    for row in response.data:
        user = row.get("users") or {}
        seniors.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "name": user.get("name"),
            "department": user.get("department"),
            "graduated_year": row.get("graduated_year"),
            "bio": row.get("bio"),
            "job_title": row.get("job_title"),
            "company": row.get("company"),
            "is_available": row.get("is_available"),
            "skills": row.get("skills"),
            "timetable": row.get("timetable")
        })

    return success_response(data=seniors)


async def get_senior(senior_id: str, supabase):
    # 기본 프로필 조회
    try:
        senior = (
            supabase.table("senior_profiles")
            .select("id, user_id, bio, job_title, company, graduated_year, skills, is_available, users(name, department), timetable")
            .eq("id", senior_id)
            .maybe_single()
            .execute()
        )
    except APIError:
        raise HTTPException(status_code=500, detail={"message": "선배 상세 조회에 실패했습니다.", "code": "FETCH_FAILED"})

    if not senior.data:
        raise HTTPException(status_code=404, detail={"message": "선배 프로필을 찾을 수 없습니다.", "code": "SENIOR_NOT_FOUND"})

    row = senior.data
    user = row.get("users") or {}
    senior_user_id = row["user_id"]

    # 학업 여정 그리드 조회
    curriculum = (
        supabase.table("curriculums")
        .select("year_level, semester_type, courses_master(course_name)")
        .eq("user_id", senior_user_id)
        .eq("is_representative", True)
        .order("year_level", desc=False)
        .order("semester_type", desc=False)
        .execute()
    )

    curriculum_grid = []
    for c in curriculum.data:
        course = c.get("courses_master") or {}
        curriculum_grid.append({
            "year_level": c["year_level"],
            "semester_type": c["semester_type"],
            "course_name": course.get("course_name"),
        })

    # 멘토링 가능 시간 조회
    slots = (
        supabase.table("mentoring_slots")
        .select("id, available_date, start_time, end_time")
        .eq("mentor_id", senior_user_id)
        .eq("is_reserved", False)
        .gte("available_date", date.today().isoformat())
        .order("available_date", desc=False)
        .order("start_time", desc=False)
        .execute()
    )

    return success_response(data={
        "id": row["id"],
        "user_id": senior_user_id,
        "name": user.get("name"),
        "department": user.get("department"),
        "graduated_year": row.get("graduated_year"),
        "bio": row.get("bio"),
        "job_title": row.get("job_title"),
        "company": row.get("company"),
        "is_available": row.get("is_available"),
        "curriculum_grid": curriculum_grid,
        "mentoring_slots": slots.data,
        "timetable": row.get("timetable")

    })
