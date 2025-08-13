from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str

class CreateUsers(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    age: int

class UpdateUser(BaseModel):

    name : str | None = None
    username : str | None = None
    email : str | None = None
    password : str | None = None
    age: int