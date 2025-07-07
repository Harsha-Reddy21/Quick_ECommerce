from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database.database import get_db
from app.models.models import Prescription, PrescriptionMedicine, Medicine
from app.schemas.prescription_schemas import Prescription as PrescriptionSchema, PrescriptionUpdate, PrescriptionMedicine as PrescriptionMedicineSchema, PrescriptionMedicineCreate
from app.utils.auth import get_current_active_user, get_pharmacy_admin
from app.models.models import User
from app.utils.file_upload import save_prescription

router = APIRouter()

@router.post("/upload", response_model=PrescriptionSchema)
async def upload_prescription(
    prescription_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload prescription image"""
    # Save prescription image
    image_path = await save_prescription(prescription_file)
    
    # Create prescription record
    db_prescription = Prescription(
        user_id=current_user.id,
        image_path=image_path,
        is_verified=False
    )
    
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    
    return db_prescription

@router.get("", response_model=List[PrescriptionSchema])
def get_user_prescriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's prescriptions"""
    prescriptions = db.query(Prescription).filter(
        Prescription.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return prescriptions

@router.get("/{prescription_id}", response_model=PrescriptionSchema)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific prescription details"""
    # Get prescription
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id,
        Prescription.user_id == current_user.id
    ).first()
    
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    return prescription

@router.put("/{prescription_id}/verify", response_model=PrescriptionSchema)
def verify_prescription(
    prescription_id: int,
    verification: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Verify prescription (pharmacist only)"""
    # Get prescription
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    # Update prescription
    prescription.is_verified = verification.is_verified
    prescription.verified_by = current_user.id
    
    # Set expiry date if not provided (default 30 days)
    if verification.expires_at:
        prescription.expires_at = verification.expires_at
    else:
        prescription.expires_at = datetime.utcnow() + timedelta(days=30)
    
    db.commit()
    db.refresh(prescription)
    
    return prescription

@router.post("/{prescription_id}/medicines", response_model=PrescriptionMedicineSchema)
def add_medicine_to_prescription(
    prescription_id: int,
    medicine: PrescriptionMedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Add medicine to prescription (pharmacist only)"""
    # Get prescription
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    # Check if medicine exists
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine.medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Create prescription medicine
    db_prescription_medicine = PrescriptionMedicine(
        prescription_id=prescription_id,
        medicine_id=medicine.medicine_id,
        dosage=medicine.dosage,
        quantity=medicine.quantity
    )
    
    db.add(db_prescription_medicine)
    db.commit()
    db.refresh(db_prescription_medicine)
    
    return db_prescription_medicine

@router.get("/{prescription_id}/medicines", response_model=List[PrescriptionMedicineSchema])
def get_prescription_medicines(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get medicines from prescription"""
    # Get prescription
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()
    
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    # Check if user is owner or pharmacy admin
    if prescription.user_id != current_user.id and not current_user.is_pharmacy_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this prescription")
    
    # Get prescription medicines
    prescription_medicines = db.query(PrescriptionMedicine).filter(
        PrescriptionMedicine.prescription_id == prescription_id
    ).all()
    
    return prescription_medicines 