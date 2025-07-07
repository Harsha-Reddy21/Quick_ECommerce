from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    phone: str
    full_name: str

# User Registration Schema
class UserCreate(UserBase):
    password: str
    confirm_password: str

# User Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Address Schema
class AddressBase(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# User Response Schema
class User(UserBase):
    id: int
    is_active: bool
    is_pharmacy_admin: bool = False
    is_delivery_partner: bool = False
    created_at: datetime
    addresses: List[Address] = []

    class Config:
        from_attributes = True

# Phone Verification Schema
class PhoneVerification(BaseModel):
    phone: str
    verification_code: str

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token Data Schema
class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None 