# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, disease, treatment, analytics, documents, xray, voice, chat
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("HealthAI")

# Initialize FastAPI app
app = FastAPI(
    title="HealthAI Backend",
    description="AI-powered Healthcare Assistant with 8 features + enhancements",
    version="1.0.0"
)

# Allow frontend (Vercel / Lovable.dev) to connect
origins = [
    "http://localhost:3000",              # Local dev frontend
    "https://your-frontend.vercel.app",   # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(disease.router, prefix="/disease", tags=["Disease Prediction"])
app.include_router(treatment.router, prefix="/treatment", tags=["Treatment Plan"])
app.include_router(analytics.router, prefix="/analytics", tags=["Health Analytics"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(xray.router, prefix="/xray", tags=["X-Ray Analysis"])
app.include_router(voice.router, prefix="/voice", tags=["Voice Query"])
app.include_router(chat.router, prefix="/chat", tags=["Patient Chat"])

# Root endpoint
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to HealthAI Backend 🚀"}

# Health check endpoint
@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "ok", "message": "HealthAI backend running successfully"}

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("HealthAI backend is starting up...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("HealthAI backend is shutting down...")
