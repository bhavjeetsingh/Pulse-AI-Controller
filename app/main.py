from fastapi import FastAPI
from app.config import settings

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