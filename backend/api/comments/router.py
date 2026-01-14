from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from backend.api.comments.models import Comment
from backend.api.comments.schemas.request import CommentRequestSchema, DeleteComment, UpdateComment
from backend.api.comments.schemas.response import CommentResponseData
from backend.api.posts.models import Posts
from backend.utils.database import get_db

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/comments", response_model=CommentResponseData)
def create_comment(request: CommentRequestSchema,db:Session=Depends(get_db)):
    """
    Create a comment on a post.

    Args:
        request: Comment content, user_id, and post_id.
        db: Database session (injected).

    Returns:
        CommentResponseData: The newly created comment.
    """
    comment = Comment(content=request.content, user_id=request.user_id,post_id=request.post_id)
    db.add(comment)
    db.commit()
    return comment

@router.get("/get_comments/{post_id}")
def get_comments( post_id:int,db:Session=Depends(get_db)):
    """
    List all comments for a given post.

    Args:
        post_id: ID of the post whose comments should be listed.
        db: Database session (injected).

    Returns:
        list[Comment]: Comments on the post, or
        {"message": "No comments found"} if there are none.
    """
    comments = db.query(Comment).filter_by(post_id=post_id).all()
    if comments:
        return comments
    return {"message": "No comments found"}

@router.patch("/update_comments")
def update_comments(request: UpdateComment,db:Session=Depends(get_db)):
    """
    Update the content of an existing comment.

    Args:
        request: post_id, comment_id, and the new content.
        db: Database session (injected).

    Returns:
        dict: {"message": "Comment updated successfully"} on success,
        {"message": "No comment found"} if the comment doesn't exist,
        or {"message": "No post found"} if the post doesn't exist.
    """
    post = db.query(Posts).filter(Posts.id==request.post_id).first()
    if post:
        comment = db.query(Comment).filter(Comment.id==request.comment_id).first()
        if comment:
            comment.content = request.content
            db.commit()
            return {"message": "Comment updated successfully"}

        return {"message": "No comment found"}

    return {"message": "No post found"}



@router.delete("/delete_comments")
def delete_comment(request:DeleteComment,db:Session=Depends(get_db)):
    """
    Delete a comment from a post.

    Args:
        request: post_id and comment_id identifying the comment to
            delete.
        db: Database session (injected).

    Returns:
        dict: {"message": "success"} on deletion,
        {"message": "comment not found"} if the comment doesn't exist,
        or {"message": "post not found"} if the post doesn't exist.
    """
    post = db.query(Posts).filter(Posts.id == request.post_id).first()
    if post:
        comments = db.query(Comment).filter(Comment.id==request.comment_id).first()
        if comments:
            db.delete(comments)
            db.commit()
            return {"message": "success"}
        return {"message": "comment not found"}

    return {"message": "post not found"}