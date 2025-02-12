from fastapi import FastAPI
from typing import Optional
from database import engine
from routers import ad_router
from routers import user_router
from routers import login_router
from models import ad_model
from database import Base



app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(login_router.router)
app.include_router(ad_router.router)
app.include_router(user_router.router)


