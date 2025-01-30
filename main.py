from fastapi import FastAPI
from routes.item_routes import item_routes

app = FastAPI()
app.include_router(item_routes)