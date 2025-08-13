from datetime import datetime

from pydantic import BaseModel



class Author(BaseModel):
    id: int
    name:str
    age: int

class PostResponseData(BaseModel):
    id: int
    title: str
    content: str
    author_data : Author
    published_date: datetime


class PostResponse(BaseModel):
    data:list[PostResponseData]
