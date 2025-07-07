from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routers import auth, medicines, categories, prescriptions, cart, orders, delivery

# Create FastAPI instance
app = FastAPI(
    title="Quick Commerce Medicine Delivery API",
    description="API for a medicine delivery platform with quick commerce features",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    return {"message": "Welcome to Quick Commerce Medicine Delivery API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 