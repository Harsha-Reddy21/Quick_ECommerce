from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.database import get_db
from app.models.models import Cart, CartItem, Medicine, Prescription, User
from app.schemas.cart_schemas import Cart as CartSchema, CartItemCreate, CartItem as CartItemSchema, CartItemUpdate, PrescriptionValidation
from app.utils.auth import get_current_active_user

router = APIRouter()

def get_or_create_cart(db: Session, user_id: int):
    """Get user's cart or create a new one if it doesn't exist"""
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart

def calculate_cart_total(cart: Cart):
    """Calculate total price of items in cart"""
    total = 0
    for item in cart.items:
        total += item.medicine.price * item.quantity
    
    return total

@router.get("", response_model=CartSchema)
def get_user_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's cart with prescription validation"""
    # Get or create cart
    cart = get_or_create_cart(db, current_user.id)
    
    # Calculate total
    cart_dict = CartSchema.from_orm(cart).dict()
    cart_dict["total"] = calculate_cart_total(cart)
    
    return cart_dict

@router.post("/items", response_model=CartItemSchema)
def add_medicine_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add medicine to cart"""
    # Get or create cart
    cart = get_or_create_cart(db, current_user.id)
    
    # Check if medicine exists
    medicine = db.query(Medicine).filter(Medicine.id == item.medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Check if medicine requires prescription
    if medicine.prescription_required and not item.prescription_id:
        raise HTTPException(
            status_code=400, 
            detail="This medicine requires a prescription. Please provide a prescription ID."
        )
    
    # If prescription provided, validate it
    if item.prescription_id:
        prescription = db.query(Prescription).filter(
            Prescription.id == item.prescription_id,
            Prescription.user_id == current_user.id,
            Prescription.is_verified == True
        ).first()
        
        if not prescription:
            raise HTTPException(
                status_code=400,
                detail="Invalid or unverified prescription"
            )
        
        # Check if prescription is expired
        if prescription.expires_at and prescription.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=400,
                detail="Prescription has expired"
            )
    
    # Check if medicine is already in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.medicine_id == item.medicine_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    # Create new cart item
    db_item = CartItem(
        cart_id=cart.id,
        medicine_id=item.medicine_id,
        quantity=item.quantity,
        prescription_id=item.prescription_id
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

@router.put("/items/{item_id}", response_model=CartItemSchema)
def update_cart_item(
    item_id: int,
    item_update: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update cart item quantity"""
    # Get cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Get cart item
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Update quantity
    cart_item.quantity = item_update.quantity
    
    db.commit()
    db.refresh(cart_item)
    
    return cart_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_medicine_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove medicine from cart"""
    # Get cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Get cart item
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Delete cart item
    db.delete(cart_item)
    db.commit()
    
    return None

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Clear entire cart"""
    # Get cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Delete all cart items
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    
    return None

@router.post("/validate-prescriptions", response_model=CartItemSchema)
def validate_prescription_for_medicine(
    validation: PrescriptionValidation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Validate prescription for medicine in cart"""
    # Get cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Get cart item
    cart_item = db.query(CartItem).filter(
        CartItem.id == validation.cart_item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Validate prescription
    prescription = db.query(Prescription).filter(
        Prescription.id == validation.prescription_id,
        Prescription.user_id == current_user.id,
        Prescription.is_verified == True
    ).first()
    
    if not prescription:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unverified prescription"
        )
    
    # Check if prescription is expired
    if prescription.expires_at and prescription.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Prescription has expired"
        )
    
    # Update cart item with prescription
    cart_item.prescription_id = validation.prescription_id
    
    db.commit()
    db.refresh(cart_item)
    
    return cart_item 