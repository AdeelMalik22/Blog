from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime,String
from backend.utils.database import Base


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

