from pydantic import BaseModel

class CommentRequestSchema(BaseModel):
    content :str
    user_id : int
    post_id : int

    class Config:
        orm_mode = True


class DeleteComment(BaseModel):
    post_id: int
    comment_id: int
    class Config:
        orm_mode = True


class UpdateComment(BaseModel):
    content :str
    comment_id : int
    post_id : int
