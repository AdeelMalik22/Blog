from pydantic.v1 import EmailStr
from sqlalchemy import Column ,String,Integer

from backend.utils.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(100),unique=True, nullable=False)
    email = Column(String(100),unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(255), nullable=False)
