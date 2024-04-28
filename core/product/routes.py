from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import Product
from dependencies import get_db
from .schemas import createProduct, getProduct

router = APIRouter()

@router.post('/products', status_code=status.HTTP_201_CREATED)
def create_product(product: createProduct, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(
        Product.identifier == product.identifier).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product {product.identifier} already exists"
        )

    createProduct = Product(identifier=product.identifier,
                            price=product.price, is_available=product.is_available)
    db.add(createProduct)
    db.commit()
    return {
        "message": "product created successfully"
    }

@router.get('/products/<int:id>', response_model=getProduct ,status_code=status.HTTP_200_OK)
def get_product(id: int, db: Session = Depends(get_db)):
    if id is None or id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Product ID"
        )
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {id} not found",
        )
    return product