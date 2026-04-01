# mentoring_slots 테이블
# - id: uuid (PK)
# - mentor_id: uuid (FK → senior_profiles.user_id) - 멘토링을 제공하는 선배의 ID
# - mentee_id: uuid (FK → auth.users.id) - 예약을 완료한 후배의 ID (미예약 시 NULL)
# - available_date: date - 멘토링 가능 날짜 (예: 2026-05-01)
# - start_time: time - 상담 시작 시간 (예: 10:00:00)
# - end_time: time - 상담 종료 시간 (예: 11:00:00)
# - is_reserved: boolean - 예약 완료 여부 (기본값: false)
# - created_at: timestamptz - 슬롯 생성 일시