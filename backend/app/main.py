from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat
from app.models.schemas import HealthResponse
from app.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    general_exception_handler,
)

app = FastAPI(
    title="Agentic Support System API",
    description="Multi-agent customer support system",
    version="0.1.0",
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

cors_origins = (
    settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", version="0.1.0")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True if settings.ENVIRONMENT == "development" else False,
    )
