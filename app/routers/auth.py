from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta

from app.database.supabase_client import db_service
from app.schemas.user_schemas import UserCreate, User as UserSchema, UserLogin, Token, Address as AddressSchema, AddressCreate, PhoneVerification
from app.utils.auth import authenticate_user, create_access_token, get_password_hash, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register_user(user: UserCreate):
    """Register a new user"""
    # Check if email already exists
    db_user = db_service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if phone already exists
    phone_check_response = db_service.get_client().table("users").select("*").eq("phone", user.phone).execute()
    if phone_check_response.data:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Check if passwords match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_data = {
        "email": user.email,
        "phone": user.phone,
        "hashed_password": hashed_password,
        "full_name": user.full_name,
        "is_active": True,
        "is_pharmacy_admin": False,
        "is_delivery_partner": False
    }
    
    new_user = db_service.create_user(user_data)
    
    return UserSchema(**new_user)

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
def get_current_user_profile(current_user = Depends(get_current_active_user)):
    """Get current user profile"""
    return UserSchema(**current_user)

@router.put("/profile", response_model=UserSchema)
def update_user_profile(
    user_data: UserSchema, 
    current_user = Depends(get_current_active_user)
):
    """Update user profile"""
    # Update user fields
    update_data = {
        "full_name": user_data.full_name,
        "phone": user_data.phone
    }
    
    updated_user = db_service.update_user(current_user["id"], update_data)
    
    return UserSchema(**updated_user)

@router.post("/verify-phone", response_model=UserSchema)
def verify_phone_number(
    verification: PhoneVerification,
    current_user = Depends(get_current_active_user)
):
    """Verify phone number with code"""
    # In a real application, you would validate the code against one sent via SMS
    # For this example, we'll just update the user's phone number
    
    # Check if phone already exists for another user
    phone_check_response = db_service.get_client().table("users").select("*").eq("phone", verification.phone).execute()
    if phone_check_response.data:
        for user in phone_check_response.data:
            if user["id"] != current_user["id"]:
                raise HTTPException(status_code=400, detail="Phone number already registered by another user")
    
    # Update phone
    updated_user = db_service.update_user(current_user["id"], {"phone": verification.phone})
    
    return UserSchema(**updated_user)

@router.get("/addresses", response_model=List[AddressSchema])
def get_user_addresses(current_user = Depends(get_current_active_user)):
    """Get all addresses for current user"""
    addresses_response = db_service.get_client().table("addresses").select("*").eq("user_id", current_user["id"]).execute()
    return [AddressSchema(**addr) for addr in addresses_response.data]

@router.post("/addresses", response_model=AddressSchema)
def add_user_address(
    address: AddressCreate,
    current_user = Depends(get_current_active_user)
):
    """Add new address for current user"""
    # If this is set as default, unset other default addresses
    if address.is_default:
        addresses_response = db_service.get_client().table("addresses").select("*").eq("user_id", current_user["id"]).eq("is_default", True).execute()
        for addr in addresses_response.data:
            db_service.get_client().table("addresses").update({"is_default": False}).eq("id", addr["id"]).execute()
    
    # Create new address
    address_data = {
        "user_id": current_user["id"],
        "address_line1": address.address_line1,
        "address_line2": address.address_line2,
        "city": address.city,
        "state": address.state,
        "postal_code": address.postal_code,
        "is_default": address.is_default
    }
    
    new_address_response = db_service.get_client().table("addresses").insert(address_data).execute()
    new_address = new_address_response.data[0] if new_address_response.data else None
    
    return AddressSchema(**new_address)

@router.put("/addresses/{address_id}", response_model=AddressSchema)
def update_user_address(
    address_id: int,
    address: AddressCreate,
    current_user = Depends(get_current_active_user)
):
    """Update user address"""
    # Get address
    address_response = db_service.get_client().table("addresses").select("*").eq("id", address_id).eq("user_id", current_user["id"]).execute()
    db_address = address_response.data[0] if address_response.data else None
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # If this is set as default, unset other default addresses
    if address.is_default and not db_address["is_default"]:
        addresses_response = db_service.get_client().table("addresses").select("*").eq("user_id", current_user["id"]).eq("is_default", True).execute()
        for addr in addresses_response.data:
            db_service.get_client().table("addresses").update({"is_default": False}).eq("id", addr["id"]).execute()
    
    # Update address
    address_data = {
        "address_line1": address.address_line1,
        "address_line2": address.address_line2,
        "city": address.city,
        "state": address.state,
        "postal_code": address.postal_code,
        "is_default": address.is_default
    }
    
    updated_address_response = db_service.get_client().table("addresses").update(address_data).eq("id", address_id).execute()
    updated_address = updated_address_response.data[0] if updated_address_response.data else None
    
    return AddressSchema(**updated_address)

@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_address(
    address_id: int,
    current_user = Depends(get_current_active_user)
):
    """Delete user address"""
    # Get address
    address_response = db_service.get_client().table("addresses").select("*").eq("id", address_id).eq("user_id", current_user["id"]).execute()
    db_address = address_response.data[0] if address_response.data else None
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Delete address
    db_service.get_client().table("addresses").delete().eq("id", address_id).execute()
    
    return None 