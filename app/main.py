from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.core.config import settings

# Create the FastAPI application
app = FastAPI(
    title="Async Multiplication API",
    description="An asynchronous API for multiplying two numbers with a delay",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Async Multiplication API",
        "docs": "/docs",
        "redoc": "/redoc",
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        workers=settings.API_WORKERS,
    )
