from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config import token
from dtos import user_dto
from database import get_db
from schemas import user_schema
from repository import user_repository
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/api/user",
    tags=["User"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)



@router.post('/', response_model=user_dto.UserDTO)
async def create_user(current_user: Annotated[token.TokenData, Depends(token.get_current_user)], request:user_schema.UserSchema, db: AsyncSession = Depends(get_db)):
    new_user = await user_repository.create_user(request, db)
    return new_user
