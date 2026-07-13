from fastapi import FastAPI
from app.config import settings
from fastapi import FastAPI
from app.config import settings
from app.models.database import engine, Base
from app.routers.keys import router as keys_router

app = FastAPI(
    title=settings.APP_NAME,
    description="PulseAIController",
    version="1.0.0"
)

@app.get('/health')
async def health_check():
    # load-balancer health check endpoint.
    return {
        'status': 'healthy',
        'app_name': settings.APP_NAME,
        'debug_mode': settings.DEBUG
    }

# Auto-create the virtual_keys table in the DB on startup
# (This is great for Day 2 testing; we will move to migrations in Week 4)
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.APP_NAME,
    description="PulseAIController",
    version="1.0.0"
)
# Register key router
app.include_router(keys_router)
@app.get('/health')
async def health_check():
    return {
        'status': 'healthy',
        'app_name': settings.APP_NAME,
        'debug_mode': settings.DEBUG
    }