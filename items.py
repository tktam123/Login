from fastapi import APIRouter, Depends, HTTPException, status  # APIRouter, not FastAPI
from models import ItemCreate, ItemUpdate, ItemOut
from auth import get_current_user
from database import items_db
import database  # import module so _next_id mutation is shared

router = APIRouter()  # was: app = FastAPI(...)

@router.get("/items", response_model=list[ItemOut], tags=["Items"])
async def list_items(current_user: str = Depends(get_current_user)):
    return list(items_db.values())

@router.get("/items/{item_id}", response_model=ItemOut, tags=["Items"])
async def get_item(item_id: int, current_user: str = Depends(get_current_user)):
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(payload: ItemCreate, current_user: str = Depends(get_current_user)):
    new_item = {
        "id": database._next_id,  # reference via module, not local variable
        "name": payload.name,
        "description": payload.description,
        "owner": current_user,
    }
    items_db[database._next_id] = new_item
    database._next_id += 1
    return new_item

@router.put("/items/{item_id}", response_model=ItemOut, tags=["Items"])
async def update_item(item_id: int, payload: ItemCreate, current_user: str = Depends(get_current_user)):
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item["owner"] != current_user:
        raise HTTPException(status_code=403, detail="Not allowed to edit this item")
    if payload.name is not None:
        item["name"] = payload.name
    if payload.description is not None:
        item["description"] = payload.description
    items_db[item_id] = item
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(item_id: int, current_user: str = Depends(get_current_user)):
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item["owner"] != current_user:
        raise HTTPException(status_code=403, detail="Not allowed to delete this item")
    del items_db[item_id]