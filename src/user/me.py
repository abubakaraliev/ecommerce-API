from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import User
from dependencies import get_db
from config import get_settings
from schemas import updateUser
import jwt
import bcrypt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # print("Token:", token)
    # print("Secret Key:", get_settings().SECRET_KEY)
    payload = jwt.decode(token, get_settings().SECRET_KEY,
                         algorithms=['HS256'])
    user_id: int = payload.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/me", response_model=None)
def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=None)
def update_user_me(user_update: updateUser, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.id} not found"
        )

    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if isinstance(user_update.password, str):
        hashed_password = bcrypt.hashpw(
            user_update.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')

    db.commit()
    return JSONResponse(content={"message": f"User {current_user.id} updated successfully"})


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return None
