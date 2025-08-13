from datetime import datetime

from pydantic import BaseModel


class RequestPost(BaseModel):
    title: str
    content: str
    author_id: int
    published_date: datetime