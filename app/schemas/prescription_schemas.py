from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Prescription Medicine Schemas
class PrescriptionMedicineBase(BaseModel):
    medicine_id: int
    dosage: Optional[str] = None
    quantity: int

class PrescriptionMedicineCreate(PrescriptionMedicineBase):
    pass

class PrescriptionMedicine(PrescriptionMedicineBase):
    id: int
    prescription_id: int

    class Config:
        orm_mode = True

# Prescription Schemas
class PrescriptionBase(BaseModel):
    user_id: int

class PrescriptionCreate(BaseModel):
    pass  # No fields needed as it's created from uploaded image

class PrescriptionVerify(BaseModel):
    is_verified: bool = True
    expires_at: Optional[datetime] = None

class Prescription(PrescriptionBase):
    id: int
    image_path: str
    is_verified: bool
    verified_by: Optional[int] = None
    created_at: datetime
    expires_at: Optional[datetime] = None
    prescription_medicines: List[PrescriptionMedicine] = []

    class Config:
        orm_mode = True 