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

class SubCategoryDTO(BaseModel):
    id:int
    name: str
    description: str | None = None
    created_by: str
    updated_by: str | None = None
    is_active: bool = True
    category_id: int

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