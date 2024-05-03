from fastapi import APIRouter, HTTPException, status, Request, Depends
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from config import get_settings
from sqlalchemy.orm import Session
from models import User
from dependencies import get_db
from schemas import loginUser
import bcrypt
import jwt

router = APIRouter()

def generate_token(user_id: int):
    expiration = datetime.now() + timedelta(days=1)
    payload = {
        'id': user_id,
        'exp': expiration
    }
    return jwt.encode(payload, get_settings().SECRET_KEY, algorithm='HS256')

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
    token = generate_token(user.id)
    return JSONResponse(content={
        "message": "login successful",
        "token_type": "Bearer",
        "access_token": token
    }, headers={"Authorization": f"Bearer {token}"})