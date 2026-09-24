import random
import string
from datetime import date, timedelta
from pydantic import BaseModel, Field, FutureDate, HttpUrl
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()
url_mappings = {}

class ShortenRequest(BaseModel):
    long_url: HttpUrl
    custom_alias: str | None = None
    expiration_date: FutureDate | None = Field(
        default_factory=lambda: date.today() + timedelta(days=7)
    )

def generate_short(length: int = 8) -> str:
    base62_chars = string.digits + string.ascii_letters
    return ''.join(random.choices(base62_chars, k=length))

@app.get("/")
def home():
    return {"message": "URL shortener is running"}

@app.post("/urls")
def shorten(request: ShortenRequest):
    if request.custom_alias:
        res = request.custom_alias
    else:
        res = generate_short()
    url_mappings[res] = str(request.long_url)
    return {"shortened_url": res}

@app.get("/{short_url}")
def redirect(short_url: str):
    if short_url not in url_mappings:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=url_mappings[short_url], status_code=302)
