import asyncio
import random

from app.core.exceptions import (
    PermanentDependencyFailure,
    TemporaryDependencyFailure,
)


async def retry_with_backoff(
    func,
    max_attempts: int = 3,
    base_delay: float = 0.2,
    max_delay: float = 2.0,
):
    last_exception = None
    for attempt in range(max_attempts):
        try:
            return await func()
        except PermanentDependencyFailure:
            raise
        except (TemporaryDependencyFailure, TimeoutError) as exc:
            last_exception = exc
            if attempt < max_attempts - 1:
                delay = min(base_delay * (2**attempt), max_delay)
                jitter = random.uniform(0, delay * 0.5)
                await asyncio.sleep(delay + jitter)
    raise last_exception
