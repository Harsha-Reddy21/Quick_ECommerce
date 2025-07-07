from app.database.database import engine, SessionLocal
from app.models.models import Base
from app.database.init_db import init_db

def create_tables():
    """Create database tables and initialize with sample data"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize database with sample data
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")
    print("Sample data initialized!") 