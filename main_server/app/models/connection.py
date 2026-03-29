# connections 테이블
# - id: uuid (PK)
# - requester_id: uuid (FK → users.id, 요청자)
# - senior_id: uuid (FK → senior_profiles.id, 선배)
# - status: text (pending / accepted / rejected)
# - message: text (연결 요청 메시지)
# - created_at: timestamp
