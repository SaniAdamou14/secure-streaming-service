from fastapi import APIRouter, Header, Query, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    HTTP_ERROR_MAP,
    CapacityExceeded,
    StreamingError,
)
from app.core.logging import logger
from app.core.rate_limit import RateLimitExceeded
from app.models.requests import StreamRequest
from app.services.streaming_service import create_stream

router = APIRouter(prefix="/api/v1")

active_streams: dict[str, dict] = {}


@router.post("/streams", status_code=201)
async def create_stream_endpoint(
    request: StreamRequest,
    raw_request: Request,
    x_correlation_id: str | None = Header(default=None),
    recommendation_mode: str = Query(default="success"),
):
    correlation_id = getattr(raw_request.state, "correlation_id", x_correlation_id or "")
    try:
        result = await create_stream(
            video_id=request.video_id,
            quality=request.quality.value,
            user_token=raw_request.headers.get("Authorization", "").removeprefix("Bearer "),
            correlation_id=correlation_id,
            recommendation_mode=recommendation_mode,
        )
        active_streams[result["stream_id"]] = result
        return JSONResponse(status_code=201, content=result)
    except RateLimitExceeded as exc:
        return JSONResponse(
            status_code=429,
            content={
                "error": {
                    "code": "RATE_LIMITED",
                    "message": "Too many requests.",
                    "correlation_id": correlation_id,
                }
            },
            headers={"Retry-After": str(exc.retry_after)},
        )
    except CapacityExceeded as exc:
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "code": "CAPACITY_EXCEEDED",
                    "message": exc.message,
                    "correlation_id": correlation_id,
                }
            },
            headers={"Retry-After": str(exc.retry_after)},
        )
    except StreamingError as exc:
        status_code = HTTP_ERROR_MAP.get(type(exc), 500)
        error_code = exc.__class__.__name__.upper()
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "code": error_code,
                    "message": exc.message,
                    "correlation_id": correlation_id,
                }
            },
        )
    except Exception:
        logger.exception("Unexpected error in create_stream_endpoint")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred.",
                    "correlation_id": correlation_id,
                }
            },
        )


@router.delete("/streams/{stream_id}", status_code=204)
async def delete_stream_endpoint(stream_id: str):
    if stream_id in active_streams:
        del active_streams[stream_id]
        from app.services.capacity_service import capacity_service

        await capacity_service.release()
        return JSONResponse(status_code=204, content=None)
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "NOT_FOUND",
                "message": "Stream not found.",
            }
        },
    )
