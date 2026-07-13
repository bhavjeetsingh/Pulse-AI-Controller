from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# pool_size and max_overflow implement connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=settings.DEBUG   
)

SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)

Base = declarative_base()

def get_db():
    '''
    FastaAPI dependency to get db sessions,
    ensure the session closses after the request lifecycle.
    '''
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

        