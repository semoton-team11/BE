import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    auth_router,
    profile_router,
    scrapbook_router,
    curriculum_router,
    senior_router,
    connection_router,
    message_router,
    course_router,
    schedule_router
)
from app.utils.error_handler import global_exception_handler
from dotenv import load_dotenv
load_dotenv()


server = FastAPI(title="KHUnnect")
raw_frontend_url = os.getenv("FRONTEND_URL")

origins = [
    "http://localhost:3000",
    "https://fe-henna-rho.vercel.app",
]

if raw_frontend_url:
    clean_url = raw_frontend_url.strip().rstrip("/")
    if clean_url not in origins:
        origins.append(clean_url)

origins = [o for o in origins if o]

server.add_exception_handler(Exception, global_exception_handler)

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
server.include_router(auth_router.router)
server.include_router(profile_router.router)
server.include_router(scrapbook_router.router)
server.include_router(curriculum_router.router)
server.include_router(senior_router.router)
server.include_router(connection_router.router)
server.include_router(message_router.router)
server.include_router(course_router.router)
server.include_router(schedule_router.router)


@server.get("/")
async def root():
    return {"message": "Server is Running"}
