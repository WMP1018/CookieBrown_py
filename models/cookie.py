from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float
from models.database import Base

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    creation_date = Column(DateTime, default=datetime.now)
    description = Column(String)
    price = Column(Float)

class ProductBase(BaseModel):
    name: str
    creation_date: Optional[datetime] = None
    description: Optional[str] = None
    price: float
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)