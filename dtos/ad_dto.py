from pydantic import BaseModel
from sqlalchemy import Date

class CategoryDTO(BaseModel):
    name: str
    description: str | None = None
    created_by: str
    updated_by: str | None = None
    is_active: bool = True

class SubCategoryDTO(BaseModel):
    name: str
    description: str | None = None
    created_by: str
    updated_by: str | None = None
    is_active: bool = True
    category_id: int

class AdvertisementDTO(BaseModel):
    title: str
    url: str | None 
    image_url: str | None = None
    description: str | None = None
    category_id: int
    sub_category_id: int
    location: str | None = None
    day: Date
    price: int
    transaction_type: str
    is_wanted: bool = False
    created_by: str
    updated_by: str | None = None