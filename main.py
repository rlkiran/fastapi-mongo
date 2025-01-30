from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.item_routes import item_routes

app = FastAPI()
# Allow all origins (change this to specific origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(item_routes)