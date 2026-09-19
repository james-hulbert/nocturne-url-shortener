from pydantic import BaseModel, HttpUrl

class URLCreate(BaseModel):
    target_url: str