# curriculums 테이블
# - id: uuid (PK)
# - user_id: uuid (FK → users.id)
# - course_id: uuid (FK → courses.id)
# - semester: text (수강 학기, e.g. "2024-1")
# - grade: text (성적)
# - status: text (수강완료 / 수강중 / 수강예정)
# - created_at: timestamp
