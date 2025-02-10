from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dtos import ad_dto
# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/api/ads",
    tags=["Ads"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_ads_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/", response_model=ad_dto.Ad)
async def read_ads():
    response = ad_dto.Ad(title="rasindu", body="kdkfddk", published=True)
    return response


@router.post("/category",response_model=ad_dto.CategoryDTO)
async def create_category():
    return None

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