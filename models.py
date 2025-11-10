from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    address: str
    phone_number: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    address: str
    phone_number: str

    model_config ={
        "from_attributes": True
    }
        

class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    model_config = {
        "from_attributes": True
    }



class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int

class ProductCreate(ProductBase):
    size: str | None = None
    color: str | None = None
    stock_status: bool = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class ProductImageBase(BaseModel):
    image_url: str

class ProductImageCreate(ProductImageBase):
    product_id: int

class ProductImageResponse(ProductImageBase):
    id: int
    product_id: int

    model_config = {
        "from_attributes": True
    }


class ReviewBase(BaseModel):
    rating: int
    comment: str

class ReviewCreate(ReviewBase):
    buyer_id: int
    product_id: int

class ReviewResponse(ReviewBase):
    id: int
    buyer_id: int
    product_id: int

    model_config = {
        "from_attributes": True
    }



class CartBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartCreate(CartBase):
    buyer_id: int
    product_id: int

class CartResponse(CartBase):
    id: int
    buyer_id: int
    product_id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }



class TransactionBase(BaseModel):
    amount: float
    status: str

class TransactionCreate(TransactionBase):
    buyer_id: int   

class TransactionResponse(TransactionBase):
    id: int
    buyer_id: int

    model_config = {
        "from_attributes": True
    }



class HistoryBase(BaseModel):
    quantity: int
    status: str 

class HistoryCreate(HistoryBase):
    buyer_id: int
    product_id: int
    transaction_id: int

class HistoryResponse(HistoryBase):
    id: int
    buyer_id: int
    product_id: int
    transaction_id: int

    model_config = {
        "from_attributes": True
    }