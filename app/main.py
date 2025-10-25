from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import feedback_routes, chat_routes, admin_routes

app = FastAPI(
    title="Green Wells Energies AI Support API",
    description="Backend API for Green Wells Energies AI Support Platform",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(feedback_routes.router, prefix="/feedback", tags=["Feedback"])
app.include_router(chat_routes.router, prefix="/chat", tags=["Chat"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def root():
    return {
        "message": "Green Wells Energies API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
