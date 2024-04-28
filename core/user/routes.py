from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from dependencies import get_db
from .schemas import createUser, loginUser
import bcrypt

router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(userData: createUser, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(
        userData.password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=userData.username,
                email=userData.email, password=hashed_password)
    db.add(user)
    db.commit()
    return {
        "message": "signup successful"
    }


@router.post('/login', status_code=status.HTTP_200_OK)
def login(userData: loginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == userData.username).first()
    if user is None or not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {userData.username} not found"
        )
    if not bcrypt.checkpw(userData.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = user.generate_token()
    return {
        "message": "login successful",
        "access_token": token,
        "token_type": "bearer",
    }