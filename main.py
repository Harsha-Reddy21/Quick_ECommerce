from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import routers
from app.routers import auth, medicines, categories, prescriptions, cart, orders, delivery

# Import Supabase client
from app.database.supabase_client import db_service

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI(
    title="Quick Commerce Medicine Delivery API",
    description="API for a medicine delivery platform with quick commerce features using Supabase",
    version="1.0.0"
)

# Get frontend URL from environment variable or use default for development
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [
    frontend_url,
    "https://quick-ecommerce-2.onrender.com",  # Production frontend URL
    "http://localhost:3000",  # Local development frontend
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(medicines.router, prefix="/medicines", tags=["Medicines"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(cart.router, prefix="/cart", tags=["Shopping Cart"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(delivery.router, prefix="/delivery", tags=["Delivery"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Quick Commerce Medicine Delivery API",
        "database": "Supabase",
        "status": "Connected",
        "project_url": os.getenv("SUPABASE_URL")
    }

@app.get("/health")
async def health_check():
    """Health check endpoint to verify database connectivity"""
    try:
        # Test database connection
        response = db_service.get_client().table("users").select("count").execute()
        return {
            "status": "healthy",
            "database": "connected",
            "supabase_project": os.getenv("SUPABASE_URL")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "database": "disconnected"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 