import uuid
from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from app.models.database import Base

class VirtualKey(Base):
    __tablename__ = "virtual_keys"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # store the sha 256 hash of the key for lookup
    key_hash = Column(String, unique=True, nullable=False, index=True)

    # store the prefix to identify the key in dashboard lists
    key_prefix = Column(String, nullable=False)

    # access controls & quotas
    rpm_limit = Column(Integer, default=60) # requests-per-minute
    tpm_limit = Column(Integer, default=100000) # tokens-per-minute
    
    # Corrected spelling to monthly_budget_usd
    monthly_budget_usd = Column(Numeric(10, 4), default=50.0000)

    # key status
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)
