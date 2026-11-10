from pydantic import BaseModel, ConfigDict


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


    