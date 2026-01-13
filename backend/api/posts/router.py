from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.api.posts.models import Posts, Authors
from backend.api.posts.schema.request import RequestPost
from backend.api.posts.schema.response import PostResponse
from backend.utils.database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
    )


@router.get("/get_post",response_model=PostResponse)
def get_post(db:Session=Depends(get_db)):
    """
    List all blog posts along with their author's details.

    For each post, looks up the associated author by author_id and
    nests the author's id, name, and age inside the post entry.

    Args:
        db: Database session (injected).

    Returns:
        PostResponse: Wrapper containing a list of posts with embedded
        author data.
    """
    post_response =  db.query(Posts).all()
    result = []
    for post in post_response:
        author_id = post.author_id
        author_data = db.query(Authors).filter(Authors.id == author_id).first()
        response = {
            "id":post.id,
            "title":post.title,
            "content":post.content,
            "author_data": {
                "id":author_data.id,
                "name":author_data.name,
                "age":author_data.age},
            "published_date":post.published_date
        }
        result.append(response)
    return PostResponse(data=result)


@router.post(
    "/create_post", )
def create_post(request: RequestPost, db: Session = Depends(get_db)):
    """
    Create a new blog post.

    Args:
        request: Title, content, author_id, and published_date for the
            new post.
        db: Database session (injected).

    Returns:
        dict: {"Message": "Post Created"}
    """
    post = Posts(title=request.title, content=request.content, author_id=request.author_id,published_date=request.published_date)
    db.add(post)
    db.commit()
    return {"Message": "Post Created"}


@router.delete("/delete_post/{post_id}")
def delete_post(post_id:int,db: Session = Depends(get_db)):
    """
    Delete a blog post by ID.

    Args:
        post_id: Primary key of the post to delete.
        db: Database session (injected).

    Returns:
        dict: {"Message": "Post Deleted"} on success, or
        {"Message": "Post Not Found"} if no matching post exists.
    """
    post = db.query(Posts).filter(Posts.id==post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return {"Message": "Post Deleted"}
    return {"Message": "Post Not Found"}