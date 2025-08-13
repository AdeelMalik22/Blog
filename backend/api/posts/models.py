from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from backend.utils.database import Base


class Authors(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(String(10000), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    published_date = Column(DateTime, nullable=False)
