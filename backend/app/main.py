from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.system_worker import generate_health_report
import os
import logging

# Initialize FastAPI with metadata
app = FastAPI(
    title="Hardened Infra API",
    description="A secure backend exposing container system metrics.",
    version="1.0.0"
)

# CRITICAL SECURITY STEP: CORS (Cross-Origin Resource Sharing)
# In production, we restrict this to our specific frontend container origin.
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"], # We only allow safe read methods for this system metrics endpoint
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def get_health():
    """
    HTTP GET endpoint that invokes the local system worker 
    and streams the container system health metrics.
    """
    logging.info("API endpoint /api/v1/health hit.")
    return generate_health_report()

@app.get("/")
def read_root():
    """
    Simple root endpoint to confirm API availability.
    """
    return {"message": "Secure Backend API is operational. Access /api/v1/health for metrics."}
