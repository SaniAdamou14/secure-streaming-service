from fastapi import APIRouter

from app.models.responses import DependencyStatus, HealthResponse, ReadinessResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy")


@router.get("/ready")
async def readiness_check():
    deps = DependencyStatus(catalog="available", recommendations="available")
    return ReadinessResponse(status="ready", dependencies=deps)
