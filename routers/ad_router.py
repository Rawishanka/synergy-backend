from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from dtos import ad_dto
from database import get_db
from schemas import ad_schema
from repository import ads_repository
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/api/ads",
    tags=["Ads"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_ads_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/", response_model=ad_dto.AdvertisementDTO)
async def read_ads():
    response = ad_dto.Ad(title="rasindu", body="kdkfddk", published=True)
    return response


@router.post("/category",response_model=ad_dto.CategoryDTO)
async def create_category(request:ad_schema.CategorySchema ,db:AsyncSession = Depends(get_db)):
    new_category = await ads_repository.create_category(request, db)
    return new_category


@router.get("/category",response_model=List[ad_dto.CategoryDTO])
async def get_category(db:AsyncSession = Depends(get_db)):
    category_list = await ads_repository.get_all_categories(db)
    return category_list


@router.post("/sub-category",response_model=ad_dto.SubCategoryDTO)
async def create_category(request:ad_schema.SubCategorySchema ,db:AsyncSession = Depends(get_db)):
    new_sub_category = await ads_repository.create_sub_category(request, db)
    return new_sub_category


@router.get("/sub-category",response_model=List[ad_dto.SubCategoryDTO])
async def get_category(db:AsyncSession = Depends(get_db)):
    category_list = await ads_repository.get_all_sub_categories(db)
    return category_list


@router.post("/advertisement",response_model=ad_dto.AdvertisementDTO)
async def create_ad(request:ad_schema.AdvertisementSchema ,db:AsyncSession = Depends(get_db)):
    new_ad = await ads_repository.create_ad(request, db)
    return new_ad


@router.get("/advertisement", response_model=ad_dto.AdvertisementSearchFilterDTO)
async def search_ad(
    search: Optional[str] = None,  # query param for search
    category_id: Optional[int] = None,  # query param for category_id
    sub_category_id: Optional[int] = None,  # query param for sub_category_id
    sort: Optional[str] = None,  # query param for sort
    db: AsyncSession = Depends(get_db)  # database session
):
    # Create the request object from query params
    request = ad_schema.AdvertisementSearchFilterSchema(
        search=search or "",
        category_id=category_id or 0,
        sub_category_id=sub_category_id or 0,
        sort=sort or "",
    )
    # Pass the request object to the repository
    new_ad = await ads_repository.search_ad(request, db)
    return new_ad


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_ads_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_ads_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}