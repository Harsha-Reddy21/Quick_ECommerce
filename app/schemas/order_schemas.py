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

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    medicine: Medicine

    class Config:
        from_attributes = True

# Order Tracking Schemas
class OrderTrackingBase(BaseModel):
    status: str
    location: Optional[str] = None
    notes: Optional[str] = None

class OrderTrackingCreate(OrderTrackingBase):
    order_id: int
    updated_by: int

class OrderTracking(OrderTrackingBase):
    id: int
    order_id: int
    timestamp: datetime
    updated_by: int

    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    address_id: int
    payment_method: str
    delivery_notes: Optional[str] = None

class OrderCreate(OrderBase):
    pass

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
    items: List[OrderItem] = []
    tracking_updates: List[OrderTracking] = []
    address: Address

    class Config:
        from_attributes = True

# Order Status Update Schema
class OrderStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

# Emergency Delivery Schema
class EmergencyDelivery(BaseModel):
    address_id: int
    medicine_ids: List[int]
    payment_method: str
    notes: Optional[str] = None

# Delivery Proof Schema
class DeliveryProof(BaseModel):
    image_path: str
    delivery_notes: Optional[str] = None

# Delivery Estimate Schema
class DeliveryEstimate(BaseModel):
    address_id: int
    is_emergency: bool = False

# Delivery Estimate Response Schema
class DeliveryEstimateResponse(BaseModel):
    estimated_minutes: int
    estimated_delivery_time: datetime 