def item_helper(item) -> dict:
    return {"id": str(item["_id"]), "name": item["name"], "description": item["description"]}