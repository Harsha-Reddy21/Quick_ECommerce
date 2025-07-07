from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.models import Category
from app.schemas.medicine_schemas import Category as CategorySchema, CategoryCreate
from app.utils.auth import get_current_active_user, get_pharmacy_admin
from app.models.models import User

router = APIRouter()

@router.get("", response_model=List[CategorySchema])
def get_all_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all medicine categories"""
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@router.post("", response_model=CategorySchema)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Create new category (pharmacy admin only)"""
    # Check if category already exists
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    # Create new category
    db_category = Category(
        name=category.name,
        description=category.description
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.get("/{category_id}", response_model=CategorySchema)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Get category by ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.put("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Update category (pharmacy admin only)"""
    # Get category
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if name already exists for another category
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category and existing_category.id != category_id:
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    # Update category
    db_category.name = category.name
    db_category.description = category.description
    
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_pharmacy_admin)
):
    """Delete category (pharmacy admin only)"""
    # Get category
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has medicines
    if db_category.medicines:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete category with associated medicines. Remove medicines first."
        )
    
    # Delete category
    db.delete(db_category)
    db.commit()
    
    return None 