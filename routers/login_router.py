from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from repository import login_repository
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated





router = APIRouter(
    prefix="/api/login",
    tags=["Login"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)



@router.post('/')
async def login_schema( request:Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(get_db)):
    user = await login_repository.login(request, db)
    
    return user
