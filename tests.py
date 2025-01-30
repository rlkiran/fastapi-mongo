import pytest
from models import Item
from routes.item_routes import create_item, read_item, update_item, delete_item, get_all_items
from fastapi import HTTPException
from bson import ObjectId
from database import collection
pytestmark = pytest.mark.asyncio(loop_scope="session")

# Test for creating an item
async def test_create_item():
    test_item = {"name": "Test Item", "description": "A test description"}
    response = await create_item(Item(**test_item))
    assert response["name"] == "Test Item"
    assert response["description"] == "A test description"

# Test for reading an item
async def test_read_item():
    test_item = {"name": "Read Item", "description": "Read description"}
    created_item = await create_item(Item(**test_item))
    response = await read_item(created_item["id"])
    assert response["name"] == "Read Item"
    assert response["description"] == "Read description"

# Test for reading an item that does not exist
async def test_read_item_not_found():
    invalid_item_id = str(ObjectId())  # Valid but non-existent ObjectId
    with pytest.raises(HTTPException):
        await read_item(invalid_item_id)

# Test for updating an item
async def test_update_item():
    test_item = {"name": "Update Item", "description": "Update description"}
    created_item = await create_item(Item(**test_item))
    updated_data = {"name": "Updated Item", "description": "Updated description"}
    response = await update_item(created_item["id"], Item(**updated_data))
    assert response["name"] == "Updated Item"
    assert response["description"] == "Updated description"

# Test for deleting an item
async def test_delete_item():
    test_item = {"name": "Delete Item", "description": "Delete description"}
    created_item = await create_item(Item(**test_item))
    response = await delete_item(created_item["id"])
    assert response["name"] == "Delete Item"
    assert response["description"] == "Delete description"

# Test for deleting an item that does not exist
async def test_delete_item_not_found():
    invalid_item_id = str(ObjectId())  # Valid but non-existent ObjectId
    with pytest.raises(HTTPException):
        await delete_item(invalid_item_id)

# Test for listing all items
async def test_list_items():
    # Clear the collection before testing
    await collection.delete_many({})  # Clear all documents in the collection
    
    test_item_1 = {"name": "Item 1", "description": "First item"}
    test_item_2 = {"name": "Item 2", "description": "Second item"}
    await create_item(Item(**test_item_1))
    await create_item(Item(**test_item_2))
    
    response = await get_all_items()
    assert len(response) == 2
    assert response[0]["name"] == "Item 1"
    assert response[1]["name"] == "Item 2"
