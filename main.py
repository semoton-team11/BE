# main.py - 라우터 등록만 함, DB는 건드리지 않음
from fastapi import FastAPI
from routers import profile, scrapbook, connections

app = FastAPI(title="경희대생을 위한 졸업 내비게이션")
app.include_router(profile.router)
app.include_router(scrapbook.router)
app.include_router(connections.router)