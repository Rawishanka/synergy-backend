from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dtos import ad_dto
from database import get_db
from schemas import ad_schema
from repository import ads_repository


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
async def create_category(request:ad_schema.CategorySchema ,db:Session = Depends(get_db)):
    new_category = await ads_repository.create_category(request, db)
    return new_category

@router.post("/sub-category",response_model=ad_dto.SubCategoryDTO)
async def create_category(request:ad_schema.SubCategorySchema ,db:Session = Depends(get_db)):
    new_sub_category = await ads_repository.create_sub_category(request, db)
    return new_sub_category


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