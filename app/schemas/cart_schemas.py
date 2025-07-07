from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.medicine_schemas import Medicine

# Cart Item Schemas
class CartItemBase(BaseModel):
    medicine_id: int
    quantity: int = 1
    prescription_id: Optional[int] = None

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    cart_id: int
    medicine: Medicine

    class Config:
        from_attributes = True

# Cart Schemas
class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[CartItem] = []
    total: Optional[float] = None

    class Config:
        from_attributes = True

# Cart Add Item Schema
class CartAddItem(BaseModel):
    medicine_id: int
    quantity: int = 1
    prescription_id: Optional[int] = None

# Cart Update Item Schema
class CartUpdateItem(BaseModel):
    item_id: int
    quantity: int

# Prescription Validation
class PrescriptionValidation(BaseModel):
    cart_item_id: int
    prescription_id: int 