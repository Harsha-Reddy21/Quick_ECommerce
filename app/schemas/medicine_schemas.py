from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Medicine Schemas
class MedicineBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int
    prescription_required: bool = False
    manufacturer: str
    image_url: Optional[str] = None

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None
    prescription_required: Optional[bool] = None
    manufacturer: Optional[str] = None
    image_url: Optional[str] = None

class StockUpdate(BaseModel):
    stock: int

class Medicine(MedicineBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Category

    class Config:
        orm_mode = True

# Medicine Search Query Params
class MedicineSearchParams(BaseModel):
    q: Optional[str] = None
    category: Optional[int] = None
    prescription_required: Optional[bool] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None 