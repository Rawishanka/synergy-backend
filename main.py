from fastapi import FastAPI
from typing import Optional
from database import engine
from routers import ad_router
from models import ad_model
from schemas import ad_schema



app = FastAPI()
ad_model.Base.metadata.create_all(bind=engine)
app.include_router(ad_router.router)


