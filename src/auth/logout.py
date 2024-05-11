from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from models import User
from user.me import get_current_user

router = APIRouter()

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="Authorization")
    response.delete_cookie("access_token")
    response.delete_cookie(key="session", path="/", httponly=True, samesite="Lax")
    return JSONResponse(content={"message": "Logout successful"})
