from pydantic import BaseModel, EmailStr


class UserResponseData(BaseModel):
    name : str
    username : str
    email: EmailStr
    age: int