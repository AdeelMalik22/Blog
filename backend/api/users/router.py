from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.api.users.models import User
from backend.api.users.schemas.request import CreateUsers, UpdateUser, LoginRequest
from backend.api.users.schemas.response import UserResponseData
from backend.utils.auth import authenticate_user, get_current_user
from backend.utils.database import get_db
from backend.utils.hash_password import create_access_token, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/api/v1/login")
def login(login_data: LoginRequest,db: Session = Depends(get_db)):
    """Generate Access Token"""
    user = db.query(User).filter(User.username == login_data.username).first()
    if user:
        user_response =  authenticate_user(login_data.password,user)
        token_data = {"sub":user_response.username}
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )



@router.post("/creat_users", response_model=UserResponseData)
def create_user(request:CreateUsers,db:Session= Depends(get_db),user=Depends(get_current_user)):
    email_validation = db.query(User).filter(User.email == request.email).first()
    if email_validation:
        raise HTTPException("Email already registered")
    username_validation = db.query(User).filter(User.username == request.username).first()
    if username_validation:
        raise HTTPException("Username already taken")

    hashed_password = get_password_hash(request.password)
    user_dict = request.dict()
    user_dict["password"] = hashed_password
    user = User(name=request.name, email=request.email,age=request.age,username=request.username,password=user_dict.get("password"))
    db.add(user)
    db.commit()
    return user


@router.get("/get_user", response_model=list[UserResponseData])
def get_users(db:Session= Depends(get_db),user=Depends(get_current_user)):
    users = db.query(User).all()
    if users:
        return users
    return {"message": "No users found"}

@router.put("/update_user")
def update_user(request:UpdateUser,db:Session= Depends(get_db),user=Depends(get_current_user)):
    user = db.query(User).filter(User.username == user).first()
    if user:
        if request.name is not None:
            user.name = request.name
        if request.email is not None:
            user.email = request.email
        if request.age is not None:
            user.age = request.age
        if request.username is not None:
            user.username = request.username

        db.commit()
        db.refresh(user)

        return {"message": "User updated successfully"}
    return {"message": "No user found"}


@router.delete("/delete_user/{user_id}")
def delete_users(user_id:int,db:Session= Depends(get_db)):
    user = db.query(User).filter(User.id==user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "No user found"}