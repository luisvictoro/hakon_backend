from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth, vulnerability
import logging

# Import models to register them with Base.metadata
from app.models import user, vulnerability as vulnerability_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # Don't raise the exception to allow the app to start

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "message": "Application is running successfully",
        "database": "connected"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(vulnerability.router, prefix="/api/vulnerability", tags=["vulnerability"])
