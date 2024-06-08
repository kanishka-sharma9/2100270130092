from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session,sessionmaker
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine
import models

app = FastAPI()
db_url = "sqlite:///./test.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    company: str
    rating: float
    class Config:
        orm_mode = True

@app.get("/products/", response_model=List[Product])
def get_products(category: str, min_price: float, max_price: float, top_n: int, db: Session = Depends(session_local)):
    products = db.query(models.Product).filter(
        models.Product.category == category,
        models.Product.price >= min_price,
        models.Product.price <= max_price
    ).order_by(models.Product.rating.desc()).limit(top_n).all()
    return products

@app.get("/categories/{categoryname}/products/{productid}", response_model=Product)
def get_product(categoryname: str, productid: int, db: Session = Depends(session_local)):
    product = db.query(models.Product).filter(
        models.Product.category == categoryname,
        models.Product.id == productid
    ).first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


def fetch_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
