from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Product
from dependencies import get_db
from schemas import createUser, createProduct
import bcrypt
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post('/createUser', status_code=status.HTTP_201_CREATED)
def addUser(userData: createUser, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == userData.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {userData.username} already exists"
        )
    hashed_password = bcrypt.hashpw(
        userData.password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=userData.username,
                email=userData.email, password=hashed_password)
    db.add(user)
    db.commit()
    return JSONResponse(content={"message": "User created successfully"})


@router.get('/users/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    if id <= 0:
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
    user = {"id": user.id, "username": user.username,
            "email": user.email, "password": user.password}
    return JSONResponse(content=user)


@router.get('/users', status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    users = [
        {"id": user.id, "username": user.username,
         "email": user.email, "password": user.password} for user in users]
    return JSONResponse(content=users)


@router.put('/users/{id}', status_code=status.HTTP_200_OK)
def update_user(id: int, userData: createUser, db: Session = Depends(get_db)):
    if id <= 0:
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
    hashed_password = bcrypt.hashpw(
        userData.password.encode('utf-8'), bcrypt.gensalt())
    user.username = userData.username
    user.email = userData.email
    user.password = hashed_password
    db.commit()
    return JSONResponse(content={"message": f"User {id} updated successfully"})


@router.delete('/users/{id}', status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    if id <= 0:
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
    return JSONResponse(content={"message": f"User {id} deleted successfully"})


@router.delete('/users', status_code=status.HTTP_200_OK)
def delete_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    for user in users:
        db.delete(user)
    db.commit()
    return JSONResponse(content={"message": f"All users deleted successfully"})


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
    return JSONResponse(content={"message": "product created successfully"})


@router.get('/products/{id}', status_code=status.HTTP_200_OK)
def get_product(id: int, db: Session = Depends(get_db)):
    if id <= 0:
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
    product = {"id": product.id, "identifier": product.identifier,
                "price": product.price, "is_available": product.is_available}
    return JSONResponse(content=product)


@router.get('/products', status_code=status.HTTP_200_OK)
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found",
            )
    products = [
        {"id": product.id, "identifier": product.identifier,
            "price": product.price, "is_available": product.is_available} for product in products]
    return JSONResponse(content=products)


@router.put('/products/{id}', status_code=status.HTTP_200_OK)
def update_product(id: int, productData: createProduct, db: Session = Depends(get_db)):
    if id <= 0:
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
    product.identifier = productData.identifier
    product.price = productData.price
    product.is_available = productData.is_available
    db.commit()
    return JSONResponse(content={"message": f"Product {id} updated successfully"})


@router.delete('/products', status_code=status.HTTP_200_OK)
def delete_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )
    for product in products:
        db.delete(product)
    db.commit()
    return JSONResponse(content={"message": f"All products deleted successfully"})
