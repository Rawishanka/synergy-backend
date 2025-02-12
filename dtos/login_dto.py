from pydantic import BaseModel

class LoginDTO(BaseModel):
    id:int
    first_name:str | None
    last_name:str | None
    user_name: str
    email: str
    phone_number : str
    password_hash:str
    
    class Config:
        orm_mode = True