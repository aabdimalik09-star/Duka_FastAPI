from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Product, User, Sale, SaleDetail, Purchase, Payment
from data_schemas import ProductRequest, ProductResponse, ProductUpdate



# DATABASE CONNECTION


DATABASE_URL = "sqlite:///duka_fastapi.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Create database tables
Base.metadata.create_all(bind=engine)



# DATABASE SESSION


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



# FASTAPI APPLICATION


app = FastAPI(
    title="Duka FastAPI",
    description="Duka POS API built with FastAPI",
    version="1.0"
)



# HOME ROUTE


@app.get("/")
def home():
    return {
        "message": "Welcome to Duka FastAPI",
        "version": "1.0"
    }



# CREATE PRODUCT
# POST /products


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
def create_product(
    prod: ProductRequest,
    db: Session = Depends(get_db)
):

    # Check whether user exists
    user = db.get(User, prod.user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Create product
    dbprod = Product(
        user_id=prod.user_id,
        product_name=prod.product_name,
        buying_price=prod.buying_price,
        selling_price=prod.selling_price
    )

    db.add(dbprod)
    db.commit()
    db.refresh(dbprod)

    return dbprod



# GET ALL PRODUCTS
# GET /products


@app.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products(
    user_id: int,
    db: Session = Depends(get_db)
):

    query = select(Product).where(
        Product.user_id == user_id
    )

    products = db.scalars(query).all()

    return products



# GET ONE PRODUCT
# GET /products/{product_id}


@app.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    query = select(Product).where(
        Product.id == product_id,
        Product.user_id == user_id
    )

    product = db.scalars(query).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product



# UPDATE PRODUCT
# PUT /products/{product_id}


@app.put(
    "/products/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    user_id: int,
    prod: ProductUpdate,
    db: Session = Depends(get_db)
):

    query = select(Product).where(
        Product.id == product_id,
        Product.user_id == user_id
    )

    product = db.scalars(query).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.product_name = prod.product_name
    product.buying_price = prod.buying_price
    product.selling_price = prod.selling_price

    db.commit()
    db.refresh(product)

    return product



# DELETE PRODUCT
# DELETE /products/{product_id}


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    query = select(Product).where(
        Product.id == product_id,
        Product.user_id == user_id
    )

    product = db.scalars(query).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }