from typing import List
from pydantic import BaseModel
import datetime
# from sqlalchemy import Date

class CategoryDTO(BaseModel):
    id:int
    name: str
    description: str | None = None
    created_by: str
    updated_by: str | None = None
    is_active: bool = True
    
    class Config:
        orm_mode = True
        from_attributes = True 

class SubCategoryDTO(BaseModel):
    id:int
    name: str
    description: str | None = None
    created_by: str
    updated_by: str | None = None
    is_active: bool = True
    category_id: int
    class Config:
        orm_mode = True
        from_attributes = True 

class AdvertisementDTO(BaseModel):
    id:int
    title: str
    url: str | None 
    image_url: str | None = None
    description: str | None = None
    category_id: int
    sub_category_id: int
    location: str | None = None
    day: datetime.date
    price: int
    transaction_type: str
    is_wanted: bool = False
    created_by: str
    updated_by: str | None = None
    class Config:
        orm_mode = True
        from_attributes = True 
        
class AdvertisementSearchFilterDTO (BaseModel):
    advertisements:List[AdvertisementDTO]
    total_pages : int
    current_page :int
    total_count:int
    class Config:
        orm_mode = True
    