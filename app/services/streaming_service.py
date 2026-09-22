import uuid

from app.core.exceptions import (
    AuthenticationFailure,
    AuthorizationFailure,
    ContentNotFound,
    ValidationFailure,
)
from app.core.logging import logger
from app.core.rate_limit import rate_limiter
from app.core.retry import retry_with_backoff
from app.core.security import generate_signed_url
from app.services.auth_service import authenticate_user, check_authorization
from app.services.capacity_service import capacity_service
from app.services.catalog_service import get_video
from app.services.recommendation_service import fetch_recommendations

GENERIC_RECOMMENDATIONS = ["popular-001", "popular-002"]


async def create_stream(
    video_id: str,
    quality: str,
    user_token: str,
    correlation_id: str,
    recommendation_mode: str = "success",
):
    user = authenticate_user(user_token)
    if user is None:
        raise AuthenticationFailure()

    video = get_video(video_id)
    if video is None:
        raise ContentNotFound()

    if not check_authorization(user, video, quality):
        raise AuthorizationFailure()

    if quality not in video.qualities:
        raise ValidationFailure(f"Quality {quality} not available for this video.")

    await rate_limiter.check_rate_limit(user.user_id)
    await capacity_service.acquire()

    degraded = False
    recommendations = GENERIC_RECOMMENDATIONS
    try:
        try:
            result = await retry_with_backoff(
                lambda: fetch_recommendations(video_id, mode=recommendation_mode),
                max_attempts=3,
                base_delay=0.2,
            )
            recommendations = result
        except Exception:
            degraded = True
            logger.warning(
                "Recommendations unavailable, returning fallback",
                extra={"correlation_id": correlation_id},
            )

        stream_id = uuid.uuid4().hex
        stream_url = generate_signed_url(video_id, user.user_id, quality)

        logger.info(
            "stream_created",
            extra={
                "correlation_id": correlation_id,
                "extra_data": {
                    "user_id": user.user_id,
                    "video_id": video_id,
                    "quality": quality,
                    "degraded": degraded,
                },
            },
        )

        return {
            "stream_id": stream_id,
            "video_id": video_id,
            "quality": quality,
            "stream_url": stream_url,
            "expires_in_seconds": 300,
            "recommendations": recommendations,
            "degraded": degraded,
            "correlation_id": correlation_id,
        }
    except Exception:
        await capacity_service.release()
        raise
