from sqlalchemy import Column, Integer, String, Float, LargeBinary, Boolean, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base 
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")  
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    size = Column(String, nullable=True)
    color = Column(String, nullable=True)
    stock_status = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    seller = relationship("User", backref="products")
    is_deleted = Column(Boolean, default=False)
    #category = relationship("Category", backref="products")

class ProductImage(Base):
    __tablename__ = "productimage"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    image_url = Column(String, nullable=False)


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, default=1)
    buyer = relationship("User", backref="cart_items")
    product = relationship("Product", backref="cart_items")


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    user = relationship("User", backref="transactions")


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    user = relationship("User", backref="history")
    product = relationship("Product", backref="history")
    transaction = relationship("Transaction", backref="history")

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    product = relationship("Product", backref="category")


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    user = relationship("User", backref="reviews")
    product = relationship("Product", backref="reviews")




