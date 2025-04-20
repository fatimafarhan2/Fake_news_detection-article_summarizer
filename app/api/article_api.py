
# creates modeularr ap routes 
from fastapi import APIRouter

from pydantic import BaseModel #BaseModel is from Pydantic and is used for validating request data.
from app.utils.scraper import scrape_article_content


# APIRouter() is like a mini FastAPI app that you can plug into your main app. 
# It helps you stay organized when your project grows
router=APIRouter()

class URLInput(BaseModel):
    url:str
# oute only accepts a JSON object for example {"url": "https://some-article-link.com"}


# When a client sends a POST request with a URL, this function is triggered.
@router.post("/scrape_article/")
async def scrape_single_article(url_input: URLInput):
    try:
        result=scrape_article_content(url_input.url)
        if result:
            return {"url":url_input.url,"content":result}
        return {"error": "Unable to scrape content"}
    except Exception as e:
        return {"error":str(e)}