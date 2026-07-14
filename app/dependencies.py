# app/dependencies.py
import hashlib
from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.tables import VirtualKey
from datetime import datetime

def verify_virtual_key(
    x_virtual_key: str = Header(..., description="Your virtual API key prefix: pk_live_..."),
    db: Session = Depends(get_db)
) -> VirtualKey:
    """
    Validates the X-Virtual-Key header.
    Returns the VirtualKey DB record if valid.
    """
    # 1. Generate SHA-256 hash of the incoming key
    hashed_key = hashlib.sha256(x_virtual_key.strip().encode()).hexdigest()
    
    # 2. Lookup key in database
    key_record = db.query(VirtualKey).filter(VirtualKey.key_hash == hashed_key).first()
    
    if not key_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Virtual Key provided."
        )
        
    # 3. Check status
    if not key_record.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Virtual Key is inactive."
        )
        
    # 4. Check expiration
    if key_record.expires_at and key_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Virtual Key has expired."
        )
        
    return key_record
