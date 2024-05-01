from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User
from dependencies import get_db
from schemas import createUser
import jwt

router = APIRouter()


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
