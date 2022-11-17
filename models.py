from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    author: str
    content_tags: str
    content: str
    created_date: datetime = datetime.utcnow()

class Post(BaseModel):
    post_id: int
    author: str
    content_tags: str
    content: str
    created_date: datetime
    updated_date: datetime

    