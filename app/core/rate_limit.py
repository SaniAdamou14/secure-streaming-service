import asyncio
import time
from collections import defaultdict

from app.config import settings


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def check_rate_limit(self, user_id: str) -> None:
        async with self._lock:
            now = time.time()
            window_start = now - self.window_seconds
            self._requests[user_id] = [t for t in self._requests[user_id] if t > window_start]
            if len(self._requests[user_id]) >= self.max_requests:
                retry_after = int(self._requests[user_id][0] + self.window_seconds - now)
                raise RateLimitExceeded(retry_after=retry_after)
            self._requests[user_id].append(now)


class RateLimitExceeded(Exception):
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__("Rate limit exceeded.")


rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)
