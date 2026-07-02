from fastapi import APIRouter, Depends, HTTPException, status
from models import ItemCreate, ItemOut
from auth import get_current_user
from database import SessionLocal, ItemModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=list[ItemOut], tags=["Items"])
def list_items(current_user: str = Depends(get_current_user), db=Depends(get_db)):
    return db.query(ItemModel).all()

@router.get("/get/{item_id}", response_model=ItemOut, tags=["Items"])
def get_item(item_id: int, current_user: str = Depends(get_current_user), db=Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/create", response_model=ItemOut, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(payload: ItemCreate, current_user: str = Depends(get_current_user), db=Depends(get_db)):
    item = ItemModel(name=payload.name, description=payload.description, owner=current_user)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/update/{item_id}", response_model=ItemOut, tags=["Items"])
def update_item(item_id: int, payload: ItemCreate, current_user: str = Depends(get_current_user), db=Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner != current_user:
        raise HTTPException(status_code=403, detail="Not allowed to edit this item")
    item.name        = payload.name
    item.description = payload.description
    db.commit()
    db.refresh(item)
    return item

@router.delete("/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
def delete_item(item_id: int, current_user: str = Depends(get_current_user), db=Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner != current_user:
        raise HTTPException(status_code=403, detail="Not allowed to delete this item")
    db.delete(item)
    db.commit()