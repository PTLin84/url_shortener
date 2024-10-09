from fastapi import FastAPI
from app.routers import items
from app.db.database import engine, Base

# Create the SQLite tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the item routes
app.include_router(items.router)
