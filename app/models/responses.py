from pydantic import BaseModel


class StreamResponse(BaseModel):
    stream_id: str
    video_id: str
    quality: str
    stream_url: str
    expires_in_seconds: int
    recommendations: list[str]
    degraded: bool
    correlation_id: str


class HealthResponse(BaseModel):
    status: str


class DependencyStatus(BaseModel):
    catalog: str
    recommendations: str


class ReadinessResponse(BaseModel):
    status: str
    dependencies: DependencyStatus


class ErrorResponse(BaseModel):
    error: dict
