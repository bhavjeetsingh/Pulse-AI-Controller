# app/main.py
from fastapi import FastAPI
from app.config import settings
from app.models.database import engine, Base
from app.routers.keys import router as keys_router
from app.routers.proxy import router as proxy_router

# Auto-create table definitions in database (e.g. SQLite pulseai.db)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="PulseAIController LLM Proxy",
    version="1.0.0"
)

# Register routes
app.include_router(keys_router)
app.include_router(proxy_router)

@app.get('/health')
async def health_check():
    """
    Load-balancer health check endpoint.
    """
    return {
        'status': 'healthy',
        'app_name': settings.APP_NAME,
        'debug_mode': settings.DEBUG
    }
