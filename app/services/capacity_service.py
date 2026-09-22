import asyncio

from app.config import settings
from app.core.exceptions import CapacityExceeded


class CapacityService:
    def __init__(self, max_streams: int):
        self.max_streams = max_streams
        self._active: int = 0
        self._lock = asyncio.Lock()

    @property
    def active_count(self) -> int:
        return self._active

    async def acquire(self) -> None:
        async with self._lock:
            if self._active >= self.max_streams:
                raise CapacityExceeded()
            self._active += 1

    async def release(self) -> None:
        async with self._lock:
            if self._active > 0:
                self._active -= 1

    async def release_if_acquired(self) -> None:
        await self.release()


capacity_service = CapacityService(max_streams=settings.max_active_streams)
