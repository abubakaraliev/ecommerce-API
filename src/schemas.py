from pydantic import BaseModel

class createUser(BaseModel):
    username: str
    email: str
    password: str


class loginUser(BaseModel):
    username: str
    password: str


class createProduct(BaseModel):
    identifier: str
    price: str
    is_available: bool


class getProduct(BaseModel):
    id: int
    identifier: str
    price: str
    is_available: bool
