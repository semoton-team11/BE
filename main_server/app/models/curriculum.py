# curriculums 테이블
# - id: uuid (PK)
# - user_id: uuid (FK → users.id)
# - course_id: uuid (FK → courses.id)
# - semester: text (수강 학기, e.g. "2024-1")
# - grade: text (성적)
# - status: text (수강완료 / 수강중 / 수강예정)
# - created_at: timestamp
# - year_level: integer (1, 2, 3, 4학년 구분)
# - semester_type: integer (1학기, 2학기 구분)
# - is_representative: boolean (기본값 false) /// 한 학기에 6~7과목을 듣는데, 그리드에는 1~2개만 노출 -> 선배가 체크한 것만 필터링하기 위함임.