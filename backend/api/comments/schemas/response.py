from datetime import datetime
from pydantic import BaseModel


class CommentResponseData(BaseModel):
    content: str
    user_id: int
    post_id: int
    created_at: datetime