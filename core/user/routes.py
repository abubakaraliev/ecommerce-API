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
        "token_type": "bearer"
    }
    
@router.get('/users/<int:id>', status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
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
    return user
    
@router.get('/users/all>',status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "No users found"
        )
    return users
@router.put('/users/<int:id>', status_code=status.HTTP_200_OK)
def update_user(id: int, userData: createUser, db: Session = Depends(get_db)):
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

@router.delete('/users/<int:id>', status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
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
     
@router.delete('/users/all', status_code=status.HTTP_200_OK)
def delete_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "No users found"
        )
    for item in users:
        db.delete(item)
    db.commit()
    return {
        "message": f"All users deleted successfully"
    }