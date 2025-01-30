from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models import Item
from database import collection
from helpers import item_helper

item_routes = APIRouter()

@item_routes.post("/items/", response_model=dict)
async def create_item(item: Item):
    new_item = await collection.insert_one(item.model_dump())
    created_item = await collection.find_one({"_id": new_item.inserted_id})
    return item_helper(created_item)

@item_routes.get("/items/{item_id}", response_model=dict)
async def read_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return item_helper(item)
    raise HTTPException(status_code=404, detail="Item not found")

@item_routes.get("/items/", response_model=list)
async def get_all_items():
    items = await collection.find().to_list(length=100)  # Adjust length if needed
    if items:
        return [item_helper(item) for item in items]
    raise HTTPException(status_code=404, detail="No items found")

@item_routes.put("/items/{item_id}", response_model=dict)
async def update_item(item_id: str, item: Item):
    updated_item = await collection.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": item.model_dump()},
        return_document=True
    )
    if updated_item:
        return item_helper(updated_item)
    raise HTTPException(status_code=404, detail="Item not found")

@item_routes.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    deleted_item = await collection.find_one_and_delete({"_id": ObjectId(item_id)})
    if deleted_item:
        return item_helper(deleted_item)
    raise HTTPException(status_code=404, detail="Item not found")
