from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from app.database.database import get_db
from app.models.models import User, Address
from app.schemas.user_schemas import UserCreate, User as UserSchema, UserLogin, Token, Address as AddressSchema, AddressCreate, PhoneVerification
from app.utils.auth import authenticate_user, create_access_token, get_password_hash, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if phone already exists
    db_user = db.query(User).filter(User.phone == user.phone).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Check if passwords match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user

@router.put("/profile", response_model=UserSchema)
def update_user_profile(
    user_data: UserSchema, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update user profile"""
    # Update user fields
    current_user.full_name = user_data.full_name
    current_user.phone = user_data.phone
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.post("/verify-phone", response_model=UserSchema)
def verify_phone_number(
    verification: PhoneVerification,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Verify phone number with code"""
    # In a real application, you would validate the code against one sent via SMS
    # For this example, we'll just update the user's phone number
    
    # Check if phone already exists for another user
    db_user = db.query(User).filter(User.phone == verification.phone).first()
    if db_user and db_user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Phone number already registered by another user")
    
    # Update phone
    current_user.phone = verification.phone
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/addresses", response_model=List[AddressSchema])
def get_user_addresses(current_user: User = Depends(get_current_active_user)):
    """Get all addresses for current user"""
    return current_user.addresses

@router.post("/addresses", response_model=AddressSchema)
def add_user_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add new address for current user"""
    # If this is set as default, unset other default addresses
    if address.is_default:
        for addr in current_user.addresses:
            if addr.is_default:
                addr.is_default = False
    
    # Create new address
    db_address = Address(
        user_id=current_user.id,
        address_line1=address.address_line1,
        address_line2=address.address_line2,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        is_default=address.is_default
    )
    
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    
    return db_address

@router.put("/addresses/{address_id}", response_model=AddressSchema)
def update_user_address(
    address_id: int,
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update user address"""
    # Get address
    db_address = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # If this is set as default, unset other default addresses
    if address.is_default and not db_address.is_default:
        for addr in current_user.addresses:
            if addr.is_default:
                addr.is_default = False
    
    # Update address
    db_address.address_line1 = address.address_line1
    db_address.address_line2 = address.address_line2
    db_address.city = address.city
    db_address.state = address.state
    db_address.postal_code = address.postal_code
    db_address.is_default = address.is_default
    
    db.commit()
    db.refresh(db_address)
    
    return db_address

@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete user address"""
    # Get address
    db_address = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Delete address
    db.delete(db_address)
    db.commit()
    
    return None 