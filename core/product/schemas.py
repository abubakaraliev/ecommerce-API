from pydantic import BaseModel
    
class createProduct(BaseModel):
    identifier: str
    price: str
    is_available: bool

class getProduct(BaseModel):
    id: int
    identifier: str
    price: str
    is_available: bool