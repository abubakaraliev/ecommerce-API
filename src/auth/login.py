from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from models import User
from dependencies import get_db
from schemas import loginUser
import bcrypt
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post('/login', status_code=status.HTTP_200_OK)
def login(userData: loginUser, request: Request, db: Session = Depends(get_db)):
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
    request.session['user_id'] = user.id
    return JSONResponse(content={
        "message": "login successful",
        "token_type": "session"
    })