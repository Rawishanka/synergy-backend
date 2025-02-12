from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from models import user_model
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from utils import password_manager
from config import token


async def login(request:Annotated[OAuth2PasswordRequestForm, Depends()] ,db:Session):
    user = db.query(user_model.User).filter(user_model.User.email == request.username).first()
    if(not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    is_verified = password_manager.verify_password(request.password, user.password_hash)
    if(not is_verified):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    access_token = token.create_access_token(data={"sub": user.email})
    return token.Token(access_token=access_token, token_type="bearer")