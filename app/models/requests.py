from enum import Enum

from pydantic import BaseModel, Field


class Quality(str, Enum):  # noqa: UP042
    P360 = "360p"
    P480 = "480p"
    P720 = "720p"
    P1080 = "1080p"


class StreamRequest(BaseModel):
    video_id: str = Field(..., min_length=36, max_length=36)
    quality: Quality
    resume_position_seconds: int = Field(default=0, ge=0, le=86400)
    device_id: str = Field(..., min_length=8, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    live: bool = Field(..., strict=True)
