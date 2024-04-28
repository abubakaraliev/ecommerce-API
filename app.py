import uvicorn
from db import Base, engine
from fastapi import FastAPI
from core.user.routes import router as user_router
from core.product.routes import router as product_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(product_router, prefix="/user")

Base.metadata.create_all(bind=engine)

if __name__ == "__main__" :
    uvicorn.run('app:app', host="0.0.0.0", port=9090, reload=True)