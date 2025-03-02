import base64
from fastapi import UploadFile
from sqlalchemy import func, or_
from sqlalchemy.orm import Query
from sqlalchemy.future import select
from models import ad_model
from schemas import ad_schema
from dtos import ad_dto
from sqlalchemy.ext.asyncio import AsyncSession
from utils import data_converter

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
        "updated_by": request.updated_by,
        "image_id":request.image_id
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





async def generate(db:AsyncSession):
    stmt = select(ad_model.RawListing).limit(2000)
    result = await db.execute(stmt)
    raw_listings = result.scalars().all()
    
    for raw in raw_listings:
        # Parse meta_data for date and location
        date, location = data_converter.parse_meta_data(raw.meta_data)
        
        # Parse price
        price = data_converter.parse_price(raw.price)
        
        # Parse image_urls
        image_url = data_converter.parse_image_urls(raw.image_urls)
        
        # Create new Advertisement object
        new_ad = ad_model.Advertisement(
            title=raw.title,
            description=raw.description,
            url=raw.url,
            image_url=image_url,
            location=location,
            day=date,
            price=price,
            transaction_type="sell",  # You can set this according to your logic
            is_wanted=False,
            created_by="system",      # Default value, adjust as needed
        )
        
        # Add to the session
        db.add(new_ad)
        
        # Mark RawListing as fetched
        raw.fetched = True

    # Commit all changes
    await db.commit()


async def store_image(db:AsyncSession, image:UploadFile):
    if image:
        # Read image data as binary
        image_data = await image.read()

        # Store image directly in the Image table
        new_image = ad_model.Image(filename=image.filename, image_data=image_data)
        db.add(new_image)
        await db.commit()
        await db.refresh(new_image)
        
        # Store image_id in Advertisement
        image_id = new_image.id
    else:
        image_id = None
    return image_id


async def get_user_advertisement(db:AsyncSession, id):
    import base64
from fastapi import UploadFile
from sqlalchemy import func, or_
from sqlalchemy.orm import Query
from sqlalchemy.future import select
from models import ad_model
from schemas import ad_schema
from dtos import ad_dto
from sqlalchemy.ext.asyncio import AsyncSession
from utils import data_converter


# Function to create a category
async def create_category(request: ad_schema.CategorySchema, db: AsyncSession):
    new_category = ad_model.Category(name=request.name, description=request.description, created_by=request.created_by, updated_by=request.updated_by)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


# Function to get all categories
async def get_all_categories(db: AsyncSession):
    result = await db.execute(select(ad_model.Category))
    categories = result.scalars().all()  # Get all category objects
    
    # Convert the list of Category objects to a list of CategoryDTOs
    return [ad_dto.CategoryDTO.from_orm(category) for category in categories]


# Function to get all subcategories
async def get_all_sub_categories(db: AsyncSession):
    result = await db.execute(select(ad_model.SubCategory))
    categories = result.scalars().all()  # Get all category objects

    return [ad_dto.SubCategoryDTO.from_orm(sub_category) for sub_category in categories]


# Function to create a subcategory
async def create_sub_category(request: ad_schema.SubCategorySchema, db: AsyncSession):
    new_sub_category = ad_model.SubCategory(name=request.name, description=request.description, created_by=request.created_by, updated_by=request.updated_by, category_id=request.category_id)
    db.add(new_sub_category)
    await db.commit()
    await db.refresh(new_sub_category)
    return new_sub_category


# Function to create an advertisement
async def create_ad(request: ad_schema.AdvertisementSchema, db: AsyncSession):
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
        "updated_by": request.updated_by,
        "image_id": request.image_id
    }

    new_advertisement = ad_model.Advertisement(**advertisement_data)
    db.add(new_advertisement)
    await db.commit()
    await db.refresh(new_advertisement)
    return new_advertisement


# Function to search for advertisements
async def search_ad(filter: ad_schema.AdvertisementSearchFilterSchema, db: AsyncSession):
    stmt = select(ad_model.Advertisement)

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

    if filter.sort == "price_asc":
        stmt = stmt.order_by(ad_model.Advertisement.price.asc())
    elif filter.sort == "price_desc":
        stmt = stmt.order_by(ad_model.Advertisement.price.desc())
    elif filter.sort == "date_asc":
        stmt = stmt.order_by(ad_model.Advertisement.day.asc())
    else:
        stmt = stmt.order_by(ad_model.Advertisement.day.desc())

    offset = (filter.page - 1) * filter.per_page
    stmt = stmt.offset(offset).limit(filter.per_page)

    result = await db.execute(stmt)
    advertisements = result.scalars().all()

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
    total_count = count_result.scalar() or 0
    total_pages = (total_count + filter.per_page - 1) // filter.per_page

    ads_dto_list = [ad_dto.AdvertisementDTO.from_orm(ad) for ad in advertisements]
    result = ad_dto.AdvertisementSearchFilterDTO(
        advertisements=ads_dto_list,
        total_count=total_count,
        current_page=filter.page,
        total_pages=total_pages
    )

    return result


# Function to generate advertisements from raw listings
async def generate(db: AsyncSession):
    stmt = select(ad_model.RawListing).limit(2000)
    result = await db.execute(stmt)
    raw_listings = result.scalars().all()

    for raw in raw_listings:
        date, location = data_converter.parse_meta_data(raw.meta_data)
        price = data_converter.parse_price(raw.price)
        image_url = data_converter.parse_image_urls(raw.image_urls)

        new_ad = ad_model.Advertisement(
            title=raw.title,
            description=raw.description,
            url=raw.url,
            image_url=image_url,
            location=location,
            day=date,
            price=price,
            transaction_type="sell",
            is_wanted=False,
            created_by="system",
        )

        db.add(new_ad)
        raw.fetched = True

    await db.commit()


# Function to store image
async def store_image(db: AsyncSession, image: UploadFile):
    if image:
        image_data = await image.read()
        new_image = ad_model.Image(filename=image.filename, image_data=image_data)
        db.add(new_image)
        await db.commit()
        await db.refresh(new_image)
        
        image_id = new_image.id
    else:
        image_id = None
    return image_id


# Function to get user advertisements along with images
async def get_user_advertisement(db: AsyncSession, id: int):
    stmt = (
        select(ad_model.Advertisement, ad_model.Image)
        .join(ad_model.Image, ad_model.Advertisement.image_id == ad_model.Image.id, isouter=True)
        .where(ad_model.Advertisement.user_id == id)
    )
    result = await db.execute(stmt)
    ads = result.all()

    # Format the response
    response_data = []
    for ad, image in ads:
        # Convert image data to base64 if image exists and image_data is available
        img_base64 = (
            base64.b64encode(image.image_data).decode('utf-8')  # No need to call encode('utf-8') here
            if image and image.image_data
            else None
        )

        # Append the advertisement data to the response list
        ad_dict = {
            "id": ad.id,
            "location": ad.location,
            "url": ad.url,
            "description": ad.description,
            "updated_by": ad.updated_by,
            "image_url": img_base64,  # Send Base64 encoded image
            "create_date": ad.create_date,
            "day": ad.day,
            "update_date": ad.update_date,
            "price": ad.price,
            "transaction_type": ad.transaction_type,
            "category_id": ad.category_id,
            "sub_category_id": ad.sub_category_id,
            "is_wanted": ad.is_wanted,
            "title": ad.title,
            "user_id": ad.user_id,
            "created_by": ad.created_by,
            "category": ad.category.name if ad.category else None,
            "sub_category": ad.sub_category.name if ad.sub_category else None
        }
        
        # Add the ad dictionary to the response data
        response_data.append(ad_dict)

    return response_data