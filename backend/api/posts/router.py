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
    post = Posts(title=request.title, content=request.content, author_id=request.author_id,published_date=request.published_date)
    db.add(post)
    db.commit()
    return {"Message": "Post Created"}


@router.delete("/delete_post/{post_id}")
def delete_post(post_id:int,db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id==post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return {"Message": "Post Deleted"}
    return {"Message": "Post Not Found"}