from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database.database import get_db
from app.models.models import Order, OrderItem, OrderTracking, Cart, CartItem, Medicine, Address, User
from app.schemas.order_schemas import Order as OrderSchema, OrderCreate, OrderStatusUpdate, DeliveryProof, OrderTracking as OrderTrackingSchema
from app.utils.auth import get_current_active_user, get_pharmacy_admin, get_delivery_partner
from app.utils.file_upload import save_delivery_proof
from app.routers.cart import calculate_cart_total

router = APIRouter()

@router.post("", response_model=OrderSchema)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create order from cart with delivery details"""
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Check if address exists and belongs to user
    address = db.query(Address).filter(
        Address.id == order_data.address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Calculate total amount
    total_amount = calculate_cart_total(cart)
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        address_id=order_data.address_id,
        total_amount=total_amount,
        payment_method=order_data.payment_method,
        delivery_notes=order_data.delivery_notes,
        estimated_delivery_time=datetime.utcnow() + timedelta(minutes=30)  # Default 30 min delivery
    )
    
    db.add(new_order)
    db.flush()  # Get order ID without committing
    
    # Create order items from cart items
    for cart_item in cart.items:
        # Check if medicine is in stock
        medicine = db.query(Medicine).filter(Medicine.id == cart_item.medicine_id).first()
        if medicine.stock < cart_item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {medicine.name}. Available: {medicine.stock}"
            )
        
        # Create order item
        order_item = OrderItem(
            order_id=new_order.id,
            medicine_id=cart_item.medicine_id,
            quantity=cart_item.quantity,
            unit_price=medicine.price,
            prescription_id=cart_item.prescription_id
        )
        
        # Update medicine stock
        medicine.stock -= cart_item.quantity
        
        db.add(order_item)
    
    # Create initial order tracking
    tracking = OrderTracking(
        order_id=new_order.id,
        status="pending",
        updated_by=current_user.id,
        notes="Order placed"
    )
    
    db.add(tracking)
    
    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    
    # Commit all changes
    db.commit()
    db.refresh(new_order)
    
    return new_order

@router.get("", response_model=List[OrderSchema])
def get_user_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's orders with delivery status"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).order_by(
        Order.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return orders

@router.get("/{order_id}", response_model=OrderSchema)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific order details"""
    # Get order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user is authorized to view this order
    if order.user_id != current_user.id and not (current_user.is_pharmacy_admin or current_user.is_delivery_partner):
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return order

@router.patch("/{order_id}/status", response_model=OrderSchema)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update order status (pharmacy/delivery partner)"""
    # Check if user is authorized to update order status
    if not (current_user.is_pharmacy_admin or current_user.is_delivery_partner):
        raise HTTPException(status_code=403, detail="Not authorized to update order status")
    
    # Get order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order status
    order.status = status_update.status
    
    # If status is "out_for_delivery", assign delivery partner
    if status_update.status == "out_for_delivery" and current_user.is_delivery_partner:
        order.delivery_partner_id = current_user.id
    
    # If status is "delivered", set actual delivery time
    if status_update.status == "delivered":
        order.actual_delivery_time = datetime.utcnow()
    
    # Create order tracking
    tracking = OrderTracking(
        order_id=order.id,
        status=status_update.status,
        updated_by=current_user.id,
        notes=status_update.notes
    )
    
    db.add(tracking)
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/{order_id}/track", response_model=List[OrderTrackingSchema])
def track_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Real-time order tracking"""
    # Get order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user is authorized to track this order
    if order.user_id != current_user.id and not (current_user.is_pharmacy_admin or current_user.is_delivery_partner):
        raise HTTPException(status_code=403, detail="Not authorized to track this order")
    
    # Get tracking updates
    tracking_updates = db.query(OrderTracking).filter(
        OrderTracking.order_id == order_id
    ).order_by(OrderTracking.timestamp.desc()).all()
    
    return tracking_updates

@router.post("/{order_id}/delivery-proof", response_model=OrderSchema)
async def upload_delivery_proof(
    order_id: int,
    delivery_notes: Optional[str] = None,
    proof_image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_delivery_partner)
):
    """Upload delivery confirmation"""
    # Get order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if order is assigned to this delivery partner
    if order.delivery_partner_id != current_user.id:
        raise HTTPException(status_code=403, detail="This order is not assigned to you")
    
    # Save proof image
    image_path = await save_delivery_proof(proof_image)
    
    # Update order status
    order.status = "delivered"
    order.actual_delivery_time = datetime.utcnow()
    
    # Create order tracking
    tracking = OrderTracking(
        order_id=order.id,
        status="delivered",
        updated_by=current_user.id,
        notes=f"Delivery confirmed with proof. {delivery_notes or ''}",
        location=image_path  # Using location field to store image path
    )
    
    db.add(tracking)
    db.commit()
    db.refresh(order)
    
    return order 