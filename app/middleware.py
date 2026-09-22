import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        header_id = request.headers.get("X-Correlation-ID")
        correlation_id = header_id if header_id else uuid.uuid4().hex
        request.state.correlation_id = correlation_id
        try:
            response = await call_next(request)
        except Exception:
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
        response.headers["X-Correlation-ID"] = correlation_id
        return response
