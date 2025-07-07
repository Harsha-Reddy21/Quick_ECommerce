from sqlalchemy.orm import Session
from app.models.models import User, Category
from app.utils.auth import get_password_hash

# Sample data for initial database setup
def init_db(db: Session):
    """Initialize database with sample data"""
    # Create admin user if it doesn't exist
    admin_user = db.query(User).filter(User.email == "admin@quickcommerce.com").first()
    if not admin_user:
        admin_user = User(
            email="admin@quickcommerce.com",
            phone="1234567890",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_active=True,
            is_pharmacy_admin=True
        )
        db.add(admin_user)
    
    # Create delivery partner if it doesn't exist
    delivery_user = db.query(User).filter(User.email == "delivery@quickcommerce.com").first()
    if not delivery_user:
        delivery_user = User(
            email="delivery@quickcommerce.com",
            phone="9876543210",
            hashed_password=get_password_hash("delivery123"),
            full_name="Delivery Partner",
            is_active=True,
            is_delivery_partner=True
        )
        db.add(delivery_user)
    
    # Create medicine categories if they don't exist
    categories = [
        {"name": "Pain Relief", "description": "Medicines for pain relief"},
        {"name": "Antibiotics", "description": "Medicines to treat bacterial infections"},
        {"name": "Vitamins & Supplements", "description": "Nutritional supplements"},
        {"name": "Diabetes", "description": "Medicines for diabetes management"},
        {"name": "Cold & Flu", "description": "Medicines for cold and flu symptoms"},
        {"name": "Allergy", "description": "Medicines for allergy relief"},
        {"name": "Digestive Health", "description": "Medicines for digestive issues"},
        {"name": "First Aid", "description": "First aid supplies"}
    ]
    
    for category_data in categories:
        category = db.query(Category).filter(Category.name == category_data["name"]).first()
        if not category:
            category = Category(
                name=category_data["name"],
                description=category_data["description"]
            )
            db.add(category)
    
    # Commit all changes
    db.commit() 