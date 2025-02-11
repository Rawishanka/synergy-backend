from models import ad_model
from schemas import ad_schema
from sqlalchemy.orm import Session


async def create_category(request:ad_schema.CategorySchema ,db:Session):
    new_category = ad_model.Category(name=request.name, description=request.description, created_by = request.created_by,  updated_by= request.updated_by)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

async def create_sub_category(request:ad_schema.SubCategorySchema ,db:Session):
    new_sub_category = await ad_model.SubCategory(name=request.name, description=request.description, created_by = request.created_by,  updated_by= request.updated_by, category_id=request.category_id)
    db.add(new_sub_category)
    db.commit()
    db.refresh(new_sub_category)
    return new_sub_category