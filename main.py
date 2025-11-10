from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import models
from database import engine, session, get_db
import database_models 
from models import UserCreate, UserResponse, UserLogin, ProductCreate, CartResponse, CartCreate, TransactionCreate, TransactionResponse, ProductUpdate, CartBase, CartCreate, CategoryBase, CategoryResponse, CategoryCreate, HistoryBase, HistoryCreate, HistoryResponse, ReviewResponse, ReviewCreate,ProductImageCreate, ProductImageResponse
from typing import Optional, List
from datetime import datetime
from sqlalchemy import LargeBinary
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import create_access_token, verify_password, get_current_user, verify_admin
from database_models import Category, Product, Cart, User, Transaction, History, Review, ProductImage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login/")

database_models.Base.metadata.create_all(bind=engine)

@app.get("/user/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(database_models.User).all()


@app.post("/user/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = database_models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/user/{id}", response_model=UserResponse)
def update_user(id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/user/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(database_models.User).filter(database_models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not registered. Please register first"
        )

    
    if str(user.password) != form_data.password:  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    
    token = create_access_token(data={"sub": user.username}, is_admin=user.is_admin)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user: database_models.User = Depends(get_current_user)):
    role = "Admin" if current_user.is_admin else "User"
    return {
        "message": f"Hello {current_user.username}, you are authenticated!",
        "role": role
    }
    

@app.get("/")
def welcome_message():
    return {"message": "Welcome to the E-commerce API"}




@app.post("/category/", status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return {"message": "Category created successfully", "category": db_category}


@app.get("/category/", status_code=status.HTTP_200_OK)
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"message": "Categories fetched successfully", "categories": categories}


@app.get("/category/{category_id}", status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category fetched successfully", "category": category}



@app.put("/category/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id: int, updated_category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.name = updated_category.name
    db_category.description = updated_category.description
    db.commit()
    db.refresh(db_category)
    return {"message": "Category updated successfully", "category": db_category}


@app.delete("/category/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}




@app.post("/product/", status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_admin(current_user)
    
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")


    new_product = Product(
        seller_id=1,  # TODO: replace with current logged-in user
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "status": "success",
        "message": "Product created successfully",
        "data": {
            "id": new_product.id,
            "name": new_product.name,
            "description": new_product.description,
            "price": new_product.price,
            "quantity": new_product.quantity,
            "category_id": new_product.category_id
        }
    }


@app.get("/product/", status_code=status.HTTP_200_OK)
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {
        "status": "success",
        "count": len(products),
        "data": products
    }


@app.get("/product/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "status": "success",
        "data": product
    }


@app.put("/product/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_admin(current_user)
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_product, key, value)

    db.commit()
    db.refresh(existing_product)

    return {
        "status": "success",
        "message": "Product updated successfully",
        "data": existing_product
    }


@app.delete("/product/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    verify_admin(current_user)
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {
        "status": "success",
        "message": "Product deleted successfully"
    }      



@app.post("/productimage/", response_model=dict)
def add_product_image(image: ProductImageCreate, db: Session = Depends(get_db)):
    new_image = ProductImage(
        product_id=image.product_id,
        image_url=image.image_url
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return {"message": "✅ Image added successfully", "image_id": new_image.id}



@app.get("/productimage/", response_model=list[ProductImageResponse])
def get_all_images(db: Session = Depends(get_db)):
    images = db.query(ProductImage).all()
    return images



@app.get("/productimage/{product_id}", response_model=list[ProductImageResponse])
def get_images_by_product(product_id: int, db: Session = Depends(get_db)):
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    if not images:
        raise HTTPException(status_code=404, detail="No images found for this product")
    return images



@app.delete("/productimage{image_id}", response_model=dict)
def delete_product_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    db.delete(image)
    db.commit()
    return {"message": "🗑️ Image deleted successfully"}



@app.post("/cart/", status_code=status.HTTP_201_CREATED)
def add_to_cart(cart_item: CartCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == cart_item.buyer_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if product exists
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if enough quantity available
    if cart_item.quantity > product.quantity:
        raise HTTPException(status_code=400, detail="Requested quantity exceeds available stock")

    # Check if item already exists in cart
    existing_item = db.query(Cart).filter(
        Cart.buyer_id == cart_item.buyer_id,
        Cart.product_id == cart_item.product_id
    ).first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return {
            "status": "success",
            "message": "Cart updated successfully (quantity increased)",
            "data": {
                "id": existing_item.id,
                "buyer_id": existing_item.buyer_id,
                "product_id": existing_item.product_id,
                "quantity": existing_item.quantity
            }
        }

    
    new_cart = Cart(
        buyer_id=cart_item.buyer_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return {
        "status": "success",
        "message": "Product added to cart successfully",
        "data": {
            "id": new_cart.id,
            "buyer_id": new_cart.buyer_id,
            "product_id": new_cart.product_id,
            "quantity": new_cart.quantity
        }
    }


@app.get("/cart/{buyer_id}", status_code=status.HTTP_200_OK)
def get_user_cart(buyer_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.buyer_id == buyer_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    return {
        "status": "success",
        "count": len(cart_items),
        "data": cart_items
    }


@app.put("/cart/{cart_id}", status_code=status.HTTP_200_OK)
def update_cart(cart_id: int, cart_data: CartBase, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Check stock availability
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if cart_data.quantity > product.quantity:
        raise HTTPException(status_code=400, detail="Requested quantity exceeds available stock")

    cart_item.quantity = cart_data.quantity
    db.commit()
    db.refresh(cart_item)

    return {
        "status": "success",
        "message": "Cart updated successfully",
        "data": cart_item
    }


@app.delete("/cart/{cart_id}", status_code=status.HTTP_200_OK)
def delete_cart_item(cart_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {
        "status": "success",
        "message": "Item removed from cart successfully"
    }



@app.post("/transaction/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    buyer = db.query(User).filter(User.id == transaction.buyer_id).first()
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer not found."
        )

    new_transaction = Transaction(
        buyer_id=transaction.buyer_id,
        amount=transaction.amount,
        status=transaction.status
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {
        "id": new_transaction.id,
        "buyer_id": new_transaction.buyer_id,
        "amount": new_transaction.amount,
        "status": new_transaction.status
    }



@app.get("/transaction/", response_model=list[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No transactions found."
        )
    return transactions


@app.get("/transaction/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found."
        )
    return transaction


@app.put("/transaction/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found."
        )

    transaction.amount = transaction_data.amount
    transaction.status = transaction_data.status
    transaction.buyer_id = transaction_data.buyer_id

    db.commit()
    db.refresh(transaction)

    return transaction

@app.delete("/transaction/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} not found."
        )

    db.delete(transaction)
    db.commit()

    return {"message": f"✅ Transaction ID {transaction_id} deleted successfully."}




@app.get("/history/", response_model=list[models.HistoryResponse])
def get_transaction_history(transaction_id: int, db: Session = Depends(get_db)):
    history = db.query(History).all()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No transaction history found."
        )
    return history

@app.post("/history/", response_model=models.HistoryCreate, status_code=status.HTTP_201_CREATED)
def create_history(history_data: models.HistoryCreate, db: Session = Depends(get_db)):
    buyer = db.query(User).filter(User.id == history_data.buyer_id).first()
    product = db.query(Product).filter(Product.id == history_data.product_id).first()
    transaction = db.query(Transaction).filter(Transaction.id == history_data.transaction_id).first()

    if not buyer or not product or not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer, Product, or Transaction not found."
        )

    new_history = History(
        buyer_id=history_data.buyer_id,
        product_id=history_data.product_id,
        transaction_id=history_data.transaction_id,
        quantity=history_data.quantity,
        status=history_data.status
    )

    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return new_history

@app.get("/history/{history_id}", response_model=models.HistoryResponse)
def get_history_by_id(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History with ID {history_id} not found."
        )
    return history

@app.delete("/history/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History with ID {history_id} not found."
        )

    db.delete(history)
    db.commit()

    return {"message": f"✅ History ID {history_id} deleted successfully."}








@app.post("/review/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # Check if buyer exists
    buyer = db.query(User).filter(User.id == review.buyer_id).first()
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="❌ Buyer not found."
        )

    # Check if product exists
    product = db.query(Product).filter(Product.id == review.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="❌ Product not found."
        )

    # Check if buyer already reviewed this product
    existing_review = db.query(Review).filter(
        Review.buyer_id == review.buyer_id,
        Review.product_id == review.product_id
    ).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="⚠️ You have already reviewed this product."
        )

    new_review = Review(
        buyer_id=review.buyer_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {
        "id": new_review.id,
        "buyer_id": new_review.buyer_id,
        "product_id": new_review.product_id,
        "rating": new_review.rating,
        "comment": new_review.comment
    }


@app.get("/review/", response_model=list[ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="⚠️ No reviews found."
        )
    return reviews


@app.get("/review/{product_id}", response_model=ReviewResponse)
def get_review(product_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == product_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"❌ Review with ID {product_id} not found."
        )
    return review


@app.put("/review/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, updated_data: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"❌ Review with ID {review_id} not found."
        )

    '''review.rating = updated_data.rating
    review.comment = updated_data.comment
    review.buyer_id = updated_data.buyer_id
    review.product_id = updated_data.product_id

    db.commit()
    db.refresh(review)

    return review'''

    updated_review = Review(
        buyer_id=review.buyer_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(updated_review)
    db.commit()
    db.refresh(updated_review)

    return {
        "id": updated_review.id,
        "buyer_id": updated_review.buyer_id,
        "product_id": updated_review.product_id,
        "rating": updated_review.rating,
        "comment": updated_review.comment
    }


@app.delete("/review/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"❌ Review with ID {review_id} not found."
        )

    db.delete(review)
    db.commit()

    return {"message": f"✅ Review ID {review_id} deleted successfully."}