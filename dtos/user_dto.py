from pydantic import BaseModel

class UserDTO(BaseModel):
    id:int
    first_name:str | None
    last_name:str | None
    user_name: str
    email: str
    phone_number : str
    is_admin:bool=False
    created_by: str
    updated_by: str | None = None
    is_active: bool = True
    password_hash:str
    class Config:
        orm_mode = True
        #exclude = {"password_hash"}