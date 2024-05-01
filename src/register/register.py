from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from dependencies import get_db
from ..schemas import createUser
import bcrypt

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(userData: createUser, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == userData.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{userData.username} already registered"
        )
    hashed_password = bcrypt.hashpw(
        userData.password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=userData.username,
                email=userData.email, password=hashed_password)
    db.add(user)
    db.commit()
    return {
        "message": "signup successful"
    }