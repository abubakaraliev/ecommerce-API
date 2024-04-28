from sqlalchemy import Column, Boolean, String, Integer
from db import Base

class Product(Base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True, nullable=False)
    identifier = Column(String(255), index=True)
    price = Column(String(255))
    is_available = Column(Boolean)