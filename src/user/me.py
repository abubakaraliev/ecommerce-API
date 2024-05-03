from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import User
from dependencies import get_db
from config import get_settings
from schemas import createUser
import jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


@router.put('/me', status_code=status.HTTP_200_OK)
def me(id: int, userData: createUser, db: Session = Depends(get_db)):
    if id is None or id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid User ID"
        )
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {id} not found",
        )
    user.username = userData.username
    user.email = userData.email
    user.password = userData.password
    db.commit()
    return {
        "message": f"User {id} updated successfully"
    }


@router.delete('/me/delete', status_code=status.HTTP_200_OK)
def delete_me(id: int, db: Session = Depends(get_db)):
    if id is None or id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid User ID"
        )
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {id} not found",
        )
    db.delete(user)
    db.commit()
    return {
        "message": f"User {id} deleted successfully"
    }
