from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import HTTP_ERROR_MAP, StreamingError
from app.core.logging import logger
from app.middleware import CorrelationMiddleware
from app.routers import health, streaming

app = FastAPI(
    title="Secure Streaming Service",
    description="Cloud video streaming authorization API",
    version="1.0.0",
)

app.add_middleware(CorrelationMiddleware)
app.include_router(health.router)
app.include_router(streaming.router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    correlation_id = getattr(request.state, "correlation_id", "")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_FAILURE",
                "message": "Invalid request parameters.",
                "correlation_id": correlation_id,
            }
        },
    )


@app.exception_handler(StreamingError)
async def streaming_error_handler(request: Request, exc: StreamingError):
    correlation_id = getattr(request.state, "correlation_id", "")
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


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    correlation_id = getattr(request.state, "correlation_id", "")
    logger.exception("Unhandled exception")
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
