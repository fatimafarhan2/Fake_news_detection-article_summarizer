from fastapi import FastAPI
from app.api.article_api import router as article_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Fake News Detection API!"}

# Make sure this line is outside of any function and placed at the bottom
app.include_router(article_router, prefix="/article")
