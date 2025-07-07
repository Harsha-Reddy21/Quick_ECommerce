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
        from_attributes = True

# Prescription Schemas
class PrescriptionBase(BaseModel):
    user_id: int

class PrescriptionCreate(PrescriptionBase):
    image_path: str
    prescription_medicines: Optional[List[PrescriptionMedicineCreate]] = None

class PrescriptionUpdate(BaseModel):
    is_verified: bool
    verified_by: int
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
        from_attributes = True 