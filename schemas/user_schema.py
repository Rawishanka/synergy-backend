from pydantic import BaseModel
from common import user_types

class UserSchema(BaseModel):
    first_name:str | None
    last_name:str | None
    user_name: str
    email: str
    password:str
    phone_number : str
    is_admin:bool=False
    created_by: str
    updated_by: str | None = None
    is_active: bool = True