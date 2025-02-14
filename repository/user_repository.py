from models import user_model
from schemas import user_schema
from utils import password_manager
from sqlalchemy.ext.asyncio import AsyncSession




async def create_user(request:user_schema.UserSchema, db:AsyncSession):
    hash_password = password_manager.get_password_hash(request.password)
    new_user = user_model.User(
        user_name=request.user_name,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password_hash=hash_password,
        phone_number=request.phone_number,
        created_by=request.created_by,
        updated_by=request.updated_by,
        is_active=request.is_active  
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

