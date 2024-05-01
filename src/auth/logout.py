from fastapi import APIRouter,status, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post('/logout', status_code=status.HTTP_200_OK)
def logout(request: Request):
    request.session.clear()
    return JSONResponse(content={"message": "logout successful"})