from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.summarizer import text_summarizer
from app.utils.scraper import scrape_article_content
router=APIRouter()

class TextInput(BaseModel):
    text:str

class URLInput(BaseModel):
    url:str

@router.post("/summarize_article/")
async def summazrize_article(input:TextInput):
    try:
            summary=text_summarizer(input.text)
            return {"summary":summary}
     
    except Exception as e:
        return{"error": str(e)}
    

@router.post("/summarize_from_url/")
async def summarize_from_url(input: URLInput):
    try:
        article = scrape_article_content(input.url)
        if not article or not article.get("text"):
            return {"error": "Could not extract article text"}
        
        summary = text_summarizer(article["text"])
        return {
            "url": input.url,
            "title": article.get("title"),
            "summary": summary
        }
    except Exception as e:
        return {"error": str(e)}