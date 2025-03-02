from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import Date
import datetime
class CategorySchema(BaseModel):
    name: str
    description: str | None = None
    created_by: str
    updated_by: str | None = None
    is_active: bool = True

class SubCategorySchema(BaseModel):
    name: str
    description: str | None = None
    created_by: str
    updated_by: str | None = None
    is_active: bool = True
    category_id: int

class AdvertisementSchema(BaseModel):
    title: str
    url: str | None 
    image_url: str | None = None
    description: str | None = None
    category_id: int
    sub_category_id: int
    user_id:int
    location: str | None = None
    day: datetime.date
    price: int
    transaction_type: str
    is_wanted: bool = False
    created_by: str
    updated_by: str | None = None
    image_id:int|None 
    
class AdvertisementSearchFilterSchema(BaseModel):
    search: str  # Search term to match in title or description
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    sort: str  # Sorting field like "price_asc", "price_desc", etc.
    page: int = 1  # Default to page 1
    per_page: int = 10  # Default to 10 items per page
    class Config:
        orm_mode = True