from pydantic import BaseModel,EmailStr,Field
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

class UserSignup(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    username: str = Field(default=None)

    class config:
        schema = {
            "example":{
                    "email":"someone@gmail.com",
                    "password":"someonepass123",
                    "username":"writergee"
            }
        }

class UserSignin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class config:
        schema = {
            "example":{
                    "email":"someone@gmail.com",
                    "password":"someonepass123",
                   
            }
        }



