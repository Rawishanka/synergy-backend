from sqlalchemy import func, or_
from sqlalchemy.orm import Query
from sqlalchemy.future import select
from models import ad_model
from schemas import ad_schema
from dtos import ad_dto
from sqlalchemy.ext.asyncio import AsyncSession

async def create_category(request:ad_schema.CategorySchema ,db:AsyncSession):
    new_category = ad_model.Category(name=request.name, description=request.description, created_by = request.created_by,  updated_by= request.updated_by)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


async def get_all_categories(db:AsyncSession):
    result = await db.execute(select(ad_model.Category))
    categories = result.scalars().all()  # Get all category objects
    
    # Convert the list of Category objects to a list of CategoryDTOs
    return [ad_dto.CategoryDTO.from_orm(category) for category in categories]


async def get_all_sub_categories(db:AsyncSession):
    result = await db.execute(select(ad_model.SubCategory))
    categories = result.scalars().all()  # Get all category objects

    return [ad_dto.SubCategoryDTO.from_orm(sub_category) for sub_category in categories]


async def create_sub_category(request:ad_schema.SubCategorySchema ,db:AsyncSession):
    new_sub_category = ad_model.SubCategory(name=request.name, description=request.description, created_by = request.created_by,  updated_by= request.updated_by, category_id=request.category_id)
    db.add(new_sub_category)
    await db.commit()
    await db.refresh(new_sub_category)
    return new_sub_category


async def create_ad(request:ad_schema.AdvertisementSchema ,db:AsyncSession):
    #new_sub_category = ad_model.Advertisement(title=request.title,url=request.url, image_url= request.image_url, description=request.description,category_id=request.category_id, sub_category_id = request.sub_category_id, user_id=request.user_id, location=request.location, day= request.day, price = request.price, transaction_type=request.transaction_type, is_wanted = request.is_wanted,  created_by = request.created_by,  updated_by= request.updated_by)
    # Create a dictionary of the attributes
    advertisement_data = {
        "title": request.title,
        "url": request.url,
        "image_url": request.image_url,
        "description": request.description,
        "category_id": request.category_id,
        "sub_category_id": request.sub_category_id,
        "user_id": request.user_id,
        "location": request.location,
        "day": request.day,
        "price": request.price,
        "transaction_type": request.transaction_type,
        "is_wanted": request.is_wanted,
        "created_by": request.created_by,
        "updated_by": request.updated_by
    }

    # Pass the dictionary to the model constructor using unpacking
    new_advertisement = ad_model.Advertisement(**advertisement_data)
    db.add(new_advertisement)
    await db.commit()
    await db.refresh(new_advertisement)
    return new_advertisement


async def search_ad(filter:ad_schema.AdvertisementSearchFilterSchema ,db:AsyncSession):
    stmt = select(ad_model.Advertisement)  # Use select() instead of query()

    # Apply filters
    if filter.search:
        stmt = stmt.where(
            or_(
                ad_model.Advertisement.title.ilike(f"%{filter.search}%"),
                ad_model.Advertisement.description.ilike(f"%{filter.search}%")
            )
        )

    if filter.category_id:
        stmt = stmt.where(ad_model.Advertisement.category_id == filter.category_id)

    if filter.sub_category_id:
        stmt = stmt.where(ad_model.Advertisement.sub_category_id == filter.sub_category_id)

    # Sorting
    if filter.sort == "price_asc":
        stmt = stmt.order_by(ad_model.Advertisement.price.asc())
    elif filter.sort == "price_desc":
        stmt = stmt.order_by(ad_model.Advertisement.price.desc())
    elif filter.sort == "date_asc":
        stmt = stmt.order_by(ad_model.Advertisement.day.asc())
    else:
        stmt = stmt.order_by(ad_model.Advertisement.day.desc())

    # Pagination logic
    offset = (filter.page - 1) * filter.per_page
    stmt = stmt.offset(offset).limit(filter.per_page)

    # Execute query for fetching data
    result = await db.execute(stmt)
    advertisements = result.scalars().all()

    # Count total matching ads
    count_stmt = select(func.count()).select_from(ad_model.Advertisement)

    if filter.search:
        count_stmt = count_stmt.where(
            or_(
                ad_model.Advertisement.title.ilike(f"%{filter.search}%"),
                ad_model.Advertisement.description.ilike(f"%{filter.search}%")
            )
        )

    if filter.category_id:
        count_stmt = count_stmt.where(ad_model.Advertisement.category_id == filter.category_id)

    if filter.sub_category_id:
        count_stmt = count_stmt.where(ad_model.Advertisement.sub_category_id == filter.sub_category_id)

    count_result = await db.execute(count_stmt)
    total_count = count_result.scalar() or 0  # Ensure a valid count
    total_pages = (total_count + filter.per_page - 1) // filter.per_page  # Calculate total pages

    ads_dto_list = [ad_dto.AdvertisementDTO.from_orm(ad) for ad in advertisements]
    # Return results as DTO
    result = ad_dto.AdvertisementSearchFilterDTO(
        advertisements=advertisements,
        total_count=total_count,
        current_page=filter.page,
        total_pages=total_pages
    )
    
    return result