from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.utils.hash_password import pwd_context, SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException

security = HTTPBearer()

def authenticate_user(password: str, user):
    """Authenticate a user"""
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user



def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
