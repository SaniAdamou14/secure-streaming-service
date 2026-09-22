import pytest

PREMIUM_VIDEO = "550e8400-e29b-41d4-a716-446655440000"
HEADERS_PREMIUM = {"Authorization": "Bearer test-premium-token"}


def stream_body(video_id=PREMIUM_VIDEO, quality="720p"):
    return {
        "video_id": video_id,
        "quality": quality,
        "resume_position_seconds": 0,
        "device_id": "device-7ad92d",
        "live": False,
    }


@pytest.mark.asyncio
async def test_recommendation_timeout_produces_degraded_response(client):
    response = await client.post(
        "/api/v1/streams",
        json=stream_body(),
        headers=HEADERS_PREMIUM,
        params={"recommendation_mode": "timeout"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["degraded"] is True
    assert "popular-001" in data["recommendations"]


@pytest.mark.asyncio
async def test_permanent_failure_produces_degraded_response(client):
    response = await client.post(
        "/api/v1/streams",
        json=stream_body(),
        headers=HEADERS_PREMIUM,
        params={"recommendation_mode": "permanent_failure"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["degraded"] is True


@pytest.mark.asyncio
async def test_correlation_id_appears_in_error(client):
    headers = {**HEADERS_PREMIUM, "X-Correlation-ID": "fail-test-abc"}
    response = await client.post(
        "/api/v1/streams",
        json={
            "video_id": "invalid",
            "quality": "720p",
            "resume_position_seconds": 0,
            "device_id": "device-7ad92d",
            "live": False,
        },
        headers=headers,
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["correlation_id"] == "fail-test-abc"


@pytest.mark.asyncio
async def test_no_stack_trace_in_error_response(client):
    response = await client.post(
        "/api/v1/streams",
        json={
            "video_id": "invalid",
            "quality": "720p",
            "resume_position_seconds": 0,
            "device_id": "device-7ad92d",
            "live": False,
        },
        headers=HEADERS_PREMIUM,
    )
    assert response.status_code == 422
    text = response.text
    assert "Traceback" not in text
    assert "File" not in text
