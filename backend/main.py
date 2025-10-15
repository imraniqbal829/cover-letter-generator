from fastapi import FastAPI
from app.models import cv
from app.database import engine
from app.api import router

# Create database tables
cv.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cover Letter Generator API")

# Include the API router
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cover Letter Generator API"}