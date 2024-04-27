from pydantic import BaseModel

class createUser(BaseModel):
    username: str
    email: str
    password: str

class loginUser(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str