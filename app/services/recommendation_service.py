import asyncio

from app.core.exceptions import (
    PermanentDependencyFailure,
    TemporaryDependencyFailure,
)


async def fetch_recommendations(video_id: str, mode: str = "success") -> list[str]:
    if mode == "timeout":
        await asyncio.sleep(0.01)
        raise TimeoutError("Recommendation service timed out.")

    if mode == "temporary_failure":
        raise TemporaryDependencyFailure("Recommendation service temporarily unavailable.")

    if mode == "permanent_failure":
        raise PermanentDependencyFailure("Recommendation service permanently unavailable.")

    await asyncio.sleep(0.01)
    return ["video-101", "video-204"]
