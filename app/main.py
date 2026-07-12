from fastapi import FastAPI
from app.database.database import Base, engine
from app.models.user import User
from app.routers.home import router as home_router
from app.routers.auth import router as auth_router
from app.routers.resume import router as resume_router
from app.models.resume import Resume


app=FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(home_router)
app.include_router(auth_router)
app.include_router(resume_router)


