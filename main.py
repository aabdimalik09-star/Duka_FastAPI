from fastapi import FastAPI
from sqlalchemy.orm import Session
from models import Base, Product, Sale, SaleDetail, Purchase,Payment
from sqlalchemy import create_engine, select
from data_schemas import (
    ProductRequest,
    ProductResponse,
    SaleRequest,
    SaleResponse,
    SaleDetailRequest,
    SaleDetailResponse,
    PurchaseRequest,
    PurchaseResponse,
    PaymentRequest,
    PaymentResponse
)


app = FastAPI()

# create a connection to the database using sqlalchemy engine
engine = create_engine("sqlite:///./duka_fastapi.db", echo=True)

# create tables into the database using sqlalchemy 
Base.metadata.create_all(engine)

# create a session to do sql transactions
session = Session(engine)


@app.get("/")
def home():
    return {"Duka FastAPI Version": "1.0"}

@app.post("/products", response_model=ProductResponse)
def create_product(prod: ProductRequest):
    # Store in the database
    dbprod = Product(
        user_id=prod.user_id,
        product_name=prod.product_name,
        buying_price=prod.buying_price,
        selling_price=prod.selling_price
        
    )

    session.add(dbprod)
    session.commit()
    return dbprod


@app.get("/products", response_model=list[ProductResponse])
def get_product():
    query = select(Product)
    products = session.scalars(query)

    return products


# SALE ROUTES
@app.post("/sales", response_model=SaleResponse)
def create_sale(sale: SaleRequest):

    dbsale = Sale(
        user_id=sale.user_id,
        sale_name=sale.sale_name,
        total_amount=sale.total_amount
    )

    session.add(dbsale)
    session.commit()
    session.refresh(dbsale)

    return dbsale


@app.get("/sales", response_model=list[SaleResponse])
def get_sales():

    query = select(Sale)
    sales = session.scalars(query).all()

    return sales


# SALE DETAIL ROUTES
@app.post("/sale-details", response_model=SaleDetailResponse)
def create_sale_detail(detail: SaleDetailRequest):

    dbdetail = SaleDetail(
        sale_id=detail.sale_id,
        product_id=detail.product_id,
        quantity=detail.quantity
    )

    session.add(dbdetail)
    session.commit()
    session.refresh(dbdetail)

    return dbdetail


@app.get("/sale-details", response_model=list[SaleDetailResponse])
def get_sale_details():

    query = select(SaleDetail)
    details = session.scalars(query).all()

    return details


# PURCHASE ROUTES
@app.post("/purchases", response_model=PurchaseResponse)
def create_purchase(purchase: PurchaseRequest):

    dbpurchase = Purchase(
        product_id=purchase.product_id,
        quantity=purchase.quantity,
        total_cost=purchase.total_cost
    )

    session.add(dbpurchase)
    session.commit()
    session.refresh(dbpurchase)

    return dbpurchase


@app.get("/purchases", response_model=list[PurchaseResponse])
def get_purchases():

    query = select(Purchase)
    purchases = session.scalars(query).all()

    return purchases


# PAYMENT ROUTES
@app.post("/payments", response_model=PaymentResponse)
def create_payment(payment: PaymentRequest):

    dbpayment = Payment(
        sale_id=payment.sale_id,
        amount_paid=payment.amount_paid,
        transaction_code=payment.transaction_code,
        mrid=payment.mrid,
        crid=payment.crid,
        status=payment.status,
        phone_number=payment.phone_number,
        payment_method=payment.payment_method
    )

    session.add(dbpayment)
    session.commit()
    session.refresh(dbpayment)

    return dbpayment


@app.get("/payments", response_model=list[PaymentResponse])
def get_payments():

    query = select(Payment)
    payments = session.scalars(query).all()

    return payments