import random
import string
from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()
url_mappings = {}

class ShortenRequest(BaseModel):
    long_url: HttpUrl

def generate_short(length: int = 8) -> str:
    base62_chars = string.digits + string.ascii_letters
    return ''.join(random.choices(base62_chars, k=length))

@app.get("/")
def home():
    return {"message": "URL shortener is running"}

@app.post("/urls")
def shorten(request: ShortenRequest):
    res = generate_short(8)
    url_mappings[res] = str(request.long_url)
    return {"shortened_url": res}

@app.get("/{short_url}")
def redirect(short_url: str):
    if short_url not in url_mappings:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=url_mappings[short_url], status_code=302)
