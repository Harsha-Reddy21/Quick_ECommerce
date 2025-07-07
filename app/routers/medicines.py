from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_, and_

from app.database.database import get_db
from app.models.models import Medicine, Category
from app.schemas.medicine_schemas import Medicine as MedicineSchema, MedicineCreate, MedicineUpdate, StockUpdate
from app.utils.auth import get_current_active_user, get_pharmacy_admin
from app.models.models import User
from app.utils.file_upload import save_medicine_image

router = APIRouter()

@router.get("", response_model=List[MedicineSchema])
def get_all_medicines(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all medicines with pagination"""
    medicines = db.query(Medicine).offset(skip).limit(limit).all()
    return medicines

@router.post("", response_model=MedicineSchema)
async def create_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin),
    image: Optional[UploadFile] = File(None)
):
    """Add new medicine (pharmacy admin only)"""
    # Check if category exists
    category = db.query(Category).filter(Category.id == medicine.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Create new medicine
    db_medicine = Medicine(
        name=medicine.name,
        description=medicine.description,
        price=medicine.price,
        stock=medicine.stock,
        category_id=medicine.category_id,
        prescription_required=medicine.prescription_required,
        manufacturer=medicine.manufacturer
    )
    
    # Save image if provided
    if image:
        image_path = await save_medicine_image(image)
        db_medicine.image_url = image_path
    
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    
    return db_medicine

@router.get("/{medicine_id}", response_model=MedicineSchema)
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db)
):
    """Get medicine by ID"""
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    return medicine

@router.put("/{medicine_id}", response_model=MedicineSchema)
async def update_medicine(
    medicine_id: int,
    medicine_update: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin),
    image: Optional[UploadFile] = File(None)
):
    """Update medicine details (pharmacy admin only)"""
    # Get medicine
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Check if category exists if updating
    if medicine_update.category_id is not None:
        category = db.query(Category).filter(Category.id == medicine_update.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Update medicine fields if provided
    for field, value in medicine_update.dict(exclude_unset=True).items():
        setattr(db_medicine, field, value)
    
    # Save image if provided
    if image:
        image_path = await save_medicine_image(image)
        db_medicine.image_url = image_path
    
    db.commit()
    db.refresh(db_medicine)
    
    return db_medicine

@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Remove medicine (pharmacy admin only)"""
    # Get medicine
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Delete medicine
    db.delete(db_medicine)
    db.commit()
    
    return None

@router.get("/search", response_model=List[MedicineSchema])
def search_medicines(
    q: Optional[str] = None,
    category: Optional[int] = None,
    prescription_required: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Search medicines with filters"""
    # Build query
    query = db.query(Medicine)
    
    # Apply filters
    filters = []
    
    if q:
        filters.append(or_(
            Medicine.name.ilike(f"%{q}%"),
            Medicine.description.ilike(f"%{q}%"),
            Medicine.manufacturer.ilike(f"%{q}%")
        ))
    
    if category:
        filters.append(Medicine.category_id == category)
    
    if prescription_required is not None:
        filters.append(Medicine.prescription_required == prescription_required)
    
    if min_price is not None:
        filters.append(Medicine.price >= min_price)
    
    if max_price is not None:
        filters.append(Medicine.price <= max_price)
    
    # Apply filters to query
    if filters:
        query = query.filter(and_(*filters))
    
    # Get results with pagination
    medicines = query.offset(skip).limit(limit).all()
    
    return medicines

@router.get("/{medicine_id}/alternatives", response_model=List[MedicineSchema])
def get_alternative_medicines(
    medicine_id: int,
    db: Session = Depends(get_db)
):
    """Get alternative medicines for the same condition"""
    # Get medicine
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Get alternatives from same category
    alternatives = db.query(Medicine).filter(
        Medicine.category_id == medicine.category_id,
        Medicine.id != medicine.id
    ).all()
    
    return alternatives

@router.patch("/{medicine_id}/stock", response_model=MedicineSchema)
def update_medicine_stock(
    medicine_id: int,
    stock_update: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Update medicine stock levels (pharmacy admin only)"""
    # Get medicine
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Update stock
    db_medicine.stock = stock_update.stock
    
    db.commit()
    db.refresh(db_medicine)
    
    return db_medicine 