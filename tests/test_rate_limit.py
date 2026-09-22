import asyncio

import pytest

from app.core.exceptions import CapacityExceeded
from app.services.capacity_service import CapacityService

PUBLIC_VIDEO = "70fbf379-9c34-4ec4-9d07-a3ee75d794c2"
HEADERS_BASIC = {"Authorization": "Bearer test-basic-token"}


def stream_body(video_id=PUBLIC_VIDEO, quality="1080p"):
    return {
        "video_id": video_id,
        "quality": quality,
        "resume_position_seconds": 0,
        "device_id": "device-7ad92d",
        "live": False,
    }


@pytest.mark.asyncio
async def test_requests_within_limit_accepted(client):
    for _ in range(3):
        response = await client.post("/api/v1/streams", json=stream_body(), headers=HEADERS_BASIC)
        assert response.status_code == 201


@pytest.mark.asyncio
async def test_rate_limit_exceeded(client):
    for _ in range(5):
        await client.post("/api/v1/streams", json=stream_body(), headers=HEADERS_BASIC)
    response = await client.post("/api/v1/streams", json=stream_body(), headers=HEADERS_BASIC)
    assert response.status_code == 429
    assert "Retry-After" in response.headers


@pytest.mark.asyncio
async def test_capacity_exceeded():
    service = CapacityService(max_streams=2)
    await service.acquire()
    await service.acquire()
    with pytest.raises(CapacityExceeded):
        await service.acquire()
    assert service.active_count == 2


@pytest.mark.asyncio
async def test_capacity_released_after_delete():
    service = CapacityService(max_streams=2)
    await service.acquire()
    await service.acquire()
    assert service.active_count == 2
    await service.release()
    assert service.active_count == 1


@pytest.mark.asyncio
async def test_concurrent_capacity_respected():
    service = CapacityService(max_streams=3)
    results = []

    async def try_acquire():
        try:
            await service.acquire()
            results.append("acquired")
        except Exception:
            results.append("rejected")

    tasks = [try_acquire() for _ in range(10)]
    await asyncio.gather(*tasks)
    assert results.count("acquired") == 3
    assert results.count("rejected") == 7
    assert service.active_count == 3
