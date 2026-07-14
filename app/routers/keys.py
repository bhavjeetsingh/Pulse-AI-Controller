import secrets
import hashlib
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field 
from app.models.database import get_db
from app.models.tables import VirtualKey
from typing import Optional

router = APIRouter(prefix='/keys', tags=['keys'])

# request validation schema
class KeyCreateRequest(BaseModel):
    rpm_limit: Optional[int] = Field(default=60, description="request per minute limit")
    tpm_limit: Optional[int] = Field(default=100000, description="token per minute limit")
    monthly_budget_usd: Optional[float] = Field(default=50.0, description="monthly budget in usd")
    
# response schema
class KeyCreateResponse(BaseModel):
    virtual_key: str
    key_prefix: str
    rpm_limit: int
    tpm_limit: int
    monthly_budget_usd: float

@router.post("/create", response_model=KeyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_key(req: KeyCreateRequest, db: Session = Depends(get_db)):
    # 1. Generate a secure random API key: pk_live_ + 32 hex chars
    raw_key = f"pk_live_{secrets.token_hex(16)}"
    
    # 2. Hash the key with SHA-256 for DB lookup
    hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
    
    # 3. Create a visible prefix (first 12 characters, e.g., 'pk_live_abcd')
    prefix = raw_key[:12]
    
    # 4. Save to database
    db_key = VirtualKey(
        key_hash=hashed_key,
        key_prefix=prefix,
        rpm_limit=req.rpm_limit,
        tpm_limit=req.tpm_limit,
        monthly_budget_usd=req.monthly_budget_usd
    )
    
    try:
        db.add(db_key)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save key to database: {str(e)}"
        )
        
    # 5. Return the raw_key only once at creation time
    return KeyCreateResponse(
        virtual_key=raw_key,
        key_prefix=prefix,
        rpm_limit=db_key.rpm_limit,
        tpm_limit=db_key.tpm_limit,
        monthly_budget_usd=float(db_key.monthly_budget_usd)
    )