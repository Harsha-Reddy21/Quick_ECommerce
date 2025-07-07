import os
import uuid
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

# Upload directories
UPLOAD_DIR = "uploads"
PRESCRIPTION_DIR = os.path.join(UPLOAD_DIR, "prescriptions")
DELIVERY_PROOF_DIR = os.path.join(UPLOAD_DIR, "delivery_proofs")
MEDICINE_IMAGES_DIR = os.path.join(UPLOAD_DIR, "medicines")

# Create directories if they don't exist
for directory in [PRESCRIPTION_DIR, DELIVERY_PROOF_DIR, MEDICINE_IMAGES_DIR]:
    os.makedirs(directory, exist_ok=True)

async def save_upload_file(upload_file: UploadFile, directory: str):
    """Save an uploaded file to the specified directory"""
    if not upload_file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Get file extension
    file_extension = os.path.splitext(upload_file.filename)[1]
    
    # Generate unique filename
    filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create full file path
    file_path = os.path.join(directory, filename)
    
    # Save file
    contents = await upload_file.read()
    
    # Validate image file
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()  # Verify it's a valid image
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    # Write file
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return file_path

async def save_prescription(prescription_file: UploadFile):
    """Save prescription image"""
    return await save_upload_file(prescription_file, PRESCRIPTION_DIR)

async def save_delivery_proof(delivery_proof_file: UploadFile):
    """Save delivery proof image"""
    return await save_upload_file(delivery_proof_file, DELIVERY_PROOF_DIR)

async def save_medicine_image(medicine_image_file: UploadFile):
    """Save medicine image"""
    return await save_upload_file(medicine_image_file, MEDICINE_IMAGES_DIR) 