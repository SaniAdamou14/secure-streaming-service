import pytest

PUBLIC_VIDEO = "70fbf379-9c34-4ec4-9d07-a3ee75d794c2"
PREMIUM_VIDEO = "550e8400-e29b-41d4-a716-446655440000"
PRIVATE_VIDEO = "4ad353d0-fab8-4eb4-9989-ab1f25ab9a00"
LIVE_PREMIUM_VIDEO = "e76ea484-5f96-4bf2-927d-763114eae4ce"

HEADERS_BASIC = {"Authorization": "Bearer test-basic-token"}
HEADERS_PREMIUM = {"Authorization": "Bearer test-premium-token"}
HEADERS_OWNER = {"Authorization": "Bearer test-owner-token"}
HEADERS_ADMIN = {"Authorization": "Bearer test-admin-token"}


def stream_body(video_id, quality="720p"):
    return {
        "video_id": video_id,
        "quality": quality,
        "resume_position_seconds": 0,
        "device_id": "device-7ad92d",
        "live": False,
    }


@pytest.mark.asyncio
async def test_basic_accesses_public(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PUBLIC_VIDEO, "1080p"), headers=HEADERS_BASIC
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_basic_denied_on_premium(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PREMIUM_VIDEO, "720p"), headers=HEADERS_BASIC
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_premium_accesses_premium(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PREMIUM_VIDEO, "720p"), headers=HEADERS_PREMIUM
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_owner_accesses_private(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PRIVATE_VIDEO, "720p"), headers=HEADERS_OWNER
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_other_user_denied_on_private(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PRIVATE_VIDEO, "720p"), headers=HEADERS_BASIC
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_accesses_private(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PRIVATE_VIDEO, "720p"), headers=HEADERS_ADMIN
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_missing_token_returns_401(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PUBLIC_VIDEO, "1080p"), headers={}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unknown_token_returns_401(client):
    headers = {"Authorization": "Bearer unknown-token"}
    response = await client.post(
        "/api/v1/streams", json=stream_body(PUBLIC_VIDEO, "1080p"), headers=headers
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_quality_denied(client):
    response = await client.post(
        "/api/v1/streams", json=stream_body(PRIVATE_VIDEO, "1080p"), headers=HEADERS_OWNER
    )
    assert response.status_code == 403
