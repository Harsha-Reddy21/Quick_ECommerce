from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.medicine_schemas import Medicine
from app.schemas.user_schemas import Address

# Order Item Schemas
class OrderItemBase(BaseModel):
    medicine_id: int
    quantity: int
    unit_price: float
    prescription_id: Optional[int] = None

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    medicine: Medicine

    class Config:
        orm_mode = True

# Order Tracking Schemas
class OrderTrackingBase(BaseModel):
    status: str
    location: Optional[str] = None
    notes: Optional[str] = None

class OrderTrackingCreate(OrderTrackingBase):
    pass

class OrderTracking(OrderTrackingBase):
    id: int
    order_id: int
    timestamp: datetime
    updated_by: int

    class Config:
        orm_mode = True

# Order Schemas
class OrderBase(BaseModel):
    address_id: int
    payment_method: str
    delivery_notes: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

class DeliveryProof(BaseModel):
    image_path: str
    delivery_notes: Optional[str] = None

class Order(OrderBase):
    id: int
    user_id: int
    total_amount: float
    status: str
    payment_status: str
    delivery_partner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    estimated_delivery_time: Optional[datetime] = None
    actual_delivery_time: Optional[datetime] = None
    address: Address
    items: List[OrderItem] = []
    tracking_updates: List[OrderTracking] = []

    class Config:
        orm_mode = True

# Delivery Estimate
class DeliveryEstimate(BaseModel):
    address_id: int
    is_emergency: bool = False

class DeliveryEstimateResponse(BaseModel):
    estimated_minutes: int
    estimated_delivery_time: datetime 