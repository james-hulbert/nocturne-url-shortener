from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
import uvicorn

from app.database import init_db
from app.schemas import URLCreate
from app.crud import create_url_mapping, get_url_by_code, increment_clicks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    init_db()
    yield
    # (Any shutdown code would go here if needed)


app = FastAPI(title="Micro URL Shortener", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Micro URL Shortener is running"}


@app.post("/url", status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLCreate):
    """Takes a long URL, generates a short code, and saves it to the database."""
    short_code = create_url_mapping(payload.target_url)

    return {
        "original_url": payload.target_url,
        "short_code": short_code,
        "short_url": f"http://127.0.0.1:8000/{short_code}"
    }


@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    """Looks up the short code, increments click count, and redirects the user."""
    db_row = get_url_by_code(short_code)

    if not db_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )

    increment_clicks(short_code)
    return RedirectResponse(url=db_row["original_url"])


@app.get("/stats/{short_code}")
def get_url_stats(short_code: str):
    """Retrieves analytics (original URL and total click count) for a short code."""
    db_row = get_url_by_code(short_code)

    if not db_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )

    return {
        "original_url": db_row["original_url"],
        "short_code": db_row["short_code"],
        "clicks": db_row["clicks"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)