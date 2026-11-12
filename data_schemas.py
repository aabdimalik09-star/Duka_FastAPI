from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# CREATE PRODUCT REQUEST
class ProductRequest(BaseModel):
    user_id: int
    product_name: str
    buying_price: float
    selling_price: float


# UPDATE PRODUCT REQUEST
class ProductUpdate(BaseModel):
    product_name: str
    buying_price: float
    selling_price: float


# PRODUCT RESPONSE
class ProductResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_name: str
    buying_price: float
    selling_price: float 
    created_at : datetime  


# SALE SCHEMAS
class SaleRequest(BaseModel):
    user_id: int
    sale_name: str
    total_amount: float


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    sale_name: str
    total_amount: float
    created_at: datetime


# SALE DETAIL SCHEMAS
class SaleDetailRequest(BaseModel):
    sale_id: int
    product_id: int
    quantity: int


class SaleDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sale_id: int
    product_id: int
    quantity: int


# PURCHASE SCHEMAS
class PurchaseRequest(BaseModel):
    product_id: int
    quantity: int
    total_cost: float


class PurchaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    total_cost: float
    created_at: datetime



# PAYMENT SCHEMAS
class PaymentRequest(BaseModel):
    sale_id: int
    amount_paid: float
    transaction_code: Optional[str] = None
    mrid: Optional[str] = None
    crid: Optional[str] = None
    status: str = "pending"
    phone_number: str
    payment_method: Optional[str] = None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sale_id: int
    amount_paid: float
    transaction_code: Optional[str]
    mrid: Optional[str]
    crid: Optional[str]
    status: str
    phone_number: str
    payment_method: Optional[str]
    created_at: datetime    