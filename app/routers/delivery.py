from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import random

from app.database.database import get_db
from app.models.models import User, Order, Address
from app.schemas.order_schemas import DeliveryEstimate, Order as OrderSchema, EmergencyDelivery, DeliveryEstimateResponse
from app.schemas.user_schemas import User as UserSchema
from app.utils.auth import get_current_active_user, get_pharmacy_admin, get_delivery_partner

router = APIRouter()

@router.get("/estimate", response_model=DeliveryEstimateResponse)
def get_delivery_estimate(
    estimate_data: DeliveryEstimate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get delivery time estimate"""
    # Check if address exists and belongs to user
    address = db.query(Address).filter(
        Address.id == estimate_data.address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Calculate estimated delivery time
    # In a real app, this would use distance calculation, traffic data, etc.
    # For this example, we'll use a simple random estimate between 10-30 minutes
    # with emergency orders prioritized to 10-15 minutes
    
    if estimate_data.is_emergency:
        estimated_minutes = random.randint(10, 15)
    else:
        estimated_minutes = random.randint(15, 30)
    
    estimated_delivery_time = datetime.utcnow() + timedelta(minutes=estimated_minutes)
    
    return {
        "estimated_minutes": estimated_minutes,
        "estimated_delivery_time": estimated_delivery_time
    }

@router.get("/partners", response_model=List[UserSchema])
def get_available_delivery_partners(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Get available delivery partners"""
    # Get all delivery partners
    delivery_partners = db.query(User).filter(
        User.is_delivery_partner == True,
        User.is_active == True
    ).all()
    
    return delivery_partners

@router.post("/emergency", response_model=OrderSchema)
def create_emergency_delivery(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Create emergency medicine delivery request"""
    # Get order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Mark order as emergency and update estimated delivery time
    order.estimated_delivery_time = datetime.utcnow() + timedelta(minutes=15)
    
    # Find available delivery partner (in a real app, would use location data)
    delivery_partner = db.query(User).filter(
        User.is_delivery_partner == True,
        User.is_active == True
    ).first()
    
    if not delivery_partner:
        raise HTTPException(status_code=404, detail="No delivery partners available")
    
    # Assign delivery partner
    order.delivery_partner_id = delivery_partner.id
    order.status = "processing"
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/nearby-pharmacies")
def find_nearby_pharmacies(
    latitude: float,
    longitude: float,
    radius: float = 5.0,  # km
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Find nearby pharmacies with stock"""
    # In a real app, this would use geospatial queries
    # For this example, we'll return a mock response
    
    return [
        {
            "id": 1,
            "name": "QuickMed Pharmacy",
            "address": "123 Health Street",
            "distance": 1.2,
            "has_delivery": True
        },
        {
            "id": 2,
            "name": "MediExpress",
            "address": "456 Wellness Avenue",
            "distance": 2.5,
            "has_delivery": True
        },
        {
            "id": 3,
            "name": "FastCare Pharmacy",
            "address": "789 Recovery Road",
            "distance": 3.8,
            "has_delivery": False
        }
    ] 