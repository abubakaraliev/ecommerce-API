import sys
import uvicorn
from db import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from admin.admin import router as admin_router
from user.me import router as user_router
from auth.login import router as login_router
from auth.logout import router as logout_router

from config import get_settings
settings = get_settings()

sys.path.append("..")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=f"{settings.SECRET_KEY}")

app.include_router(login_router, prefix="/auth")
app.include_router(logout_router, prefix="/auth")
app.include_router(admin_router, prefix="/admin")
app.include_router(user_router, prefix="/user")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=9090, reload=True)
