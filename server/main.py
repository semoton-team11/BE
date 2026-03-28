from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes import auth

server = FastAPI(title="경희대 졸업 내비게이션")

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
server.include_router(auth.router)


@server.get("/")
async def root():
  return {"message": "Server is Running"}
