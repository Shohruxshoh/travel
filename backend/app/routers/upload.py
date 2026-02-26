"""
File Upload Router
------------------
Handles image and media uploads for the admin panel.
Files are saved to /app/uploads/ with UUID filenames.
"""

import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.auth import require_admin

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".mp4", ".webm"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    _admin: str = Depends(require_admin),
):
    """Upload a file and return its URL."""
    # Validate extension
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Read and validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 10 MB.")

    # Save file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(content)

    return {"url": f"/api/uploads/{filename}", "filename": filename}
