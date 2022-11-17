from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    author: str
    content_tags: Optional[str]
    content: str
    date_created: datetime = datetime.utcnow()
    date_updated: Optional[datetime] 


class PostUpdate(BaseModel):
    author: Optional[str]
    content_tags: Optional[str]
    content: Optional[str]
    date_updated: datetime = datetime.utcnow()  

class Post(BaseModel):
    id: int
    author: str
    content_tags: str
    content: str
    date_created: datetime
    date_updated: Optional[datetime] 

