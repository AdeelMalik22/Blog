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
    """
    Authenticate a user and issue a JWT access token.

    Looks up the user by username, verifies the supplied password against
    the stored password hash, and returns a bearer token on success.

    Args:
        login_data: Username and password submitted by the client.
        db: Database session (injected).

    Returns:
        dict: {"access_token": <JWT string>, "token_type": "bearer"}

    Raises:
        HTTPException: 401 if the username doesn't exist or the password
            is incorrect.
    """
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
    """
    Create a new user account.

    Validates that the email and username aren't already registered,
    hashes the plaintext password, and persists the new user.

    Args:
        request: New user's name, username, email, password, and age.
        db: Database session (injected).
        user: Authenticated caller (injected); creating a user currently
            requires an existing valid access token.

    Returns:
        UserResponseData: The newly created user's public fields.

    Raises:
        HTTPException: If the email or username is already taken.
    """
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
    """
    List all registered users.

    Args:
        db: Database session (injected).
        user: Authenticated caller (injected).

    Returns:
        list[UserResponseData]: All users in the system, or a
        {"message": "No users found"} dict if there are none.
    """
    users = db.query(User).all()
    if users:
        return users
    return {"message": "No users found"}

@router.put("/update_user")
def update_user(request:UpdateUser,db:Session= Depends(get_db),user=Depends(get_current_user)):
    """
    Update the currently authenticated user's profile.

    Only fields present (non-None) in the request are updated; the
    target user is resolved from the username embedded in the caller's
    JWT, not from a path/body parameter.

    Args:
        request: Optional new values for name, email, age, and username.
        db: Database session (injected).
        user: Username of the authenticated caller (injected).

    Returns:
        dict: {"message": "User updated successfully"} on success, or
        {"message": "No user found"} if the user no longer exists.
    """
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
    """
    Delete a user by ID.

    Note: unlike the other user-management endpoints, this one has no
    auth dependency, so it is currently callable without a token.

    Args:
        user_id: Primary key of the user to delete.
        db: Database session (injected).

    Returns:
        dict: {"message": "User deleted successfully"} on success, or
        {"message": "No user found"} if no user with that ID exists.
    """
    user = db.query(User).filter(User.id==user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "No user found"}