# app/routers/proxy.py
import time
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import verify_virtual_key
from app.models.tables import VirtualKey
from app.config import settings
import litellm

# Set API keys for LiteLLM from configuration settings
litellm.api_key = settings.OPENAI_API_KEY
litellm.gemini_api_key = settings.GEMINI_API_KEY
litellm.groq_api_key = settings.GROQ_API_KEY

router = APIRouter(prefix="/v1", tags=["Proxy"])

@router.post("/chat/completions")
async def chat_completions(
    payload: dict, # accepts arbitrary JSON payloads to match OpenAI schema
    key_record: VirtualKey = Depends(verify_virtual_key)
):
    """
    Intercepts chat completion requests and proxies them to the target model.
    """
    model = payload.get("model")
    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing 'model' field in request body."
        )

    start_time = time.time()
    try:
        # Call LiteLLM async completions handler
        response = await litellm.acompletion(
            **payload
        )
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Inject our custom gateway metadata into the response
        response_dict = response.json() if hasattr(response, "json") else dict(response)
        response_dict["x_pulse"] = {
            "latency_ms": latency_ms,
            "provider": model.split("/")[0] if "/" in model else "unknown",
            "model_used": model
        }
        
        return response_dict
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream provider error: {str(e)}"
        )
