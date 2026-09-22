import pytest

PUBLIC_VIDEO = "70fbf379-9c34-4ec4-9d07-a3ee75d794c2"
HEADERS_BASIC = {"Authorization": "Bearer test-basic-token"}
HEADERS_PREMIUM = {"Authorization": "Bearer test-premium-token"}
HEADERS_OWNER = {"Authorization": "Bearer test-owner-token"}
HEADERS_ADMIN = {"Authorization": "Bearer test-admin-token"}


def valid_stream_body(video_id=PUBLIC_VIDEO, quality="1080p", live=False):
    return {
        "video_id": video_id,
        "quality": quality,
        "resume_position_seconds": 0,
        "device_id": "device-7ad92d",
        "live": live,
    }


@pytest.mark.asyncio
async def test_valid_request_accepted(client):
    response = await client.post("/api/v1/streams", json=valid_stream_body(), headers=HEADERS_BASIC)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_invalid_uuid_refused(client):
    body = valid_stream_body(video_id="not-a-valid-uuid")
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_unknown_quality_refused(client):
    body = valid_stream_body(quality="4k")
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_negative_position_refused(client):
    body = valid_stream_body()
    body["resume_position_seconds"] = -1
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_position_above_max_refused(client):
    body = valid_stream_body()
    body["resume_position_seconds"] = 86401
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_device_id_too_short(client):
    body = valid_stream_body()
    body["device_id"] = "short"
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_device_id_too_long(client):
    body = valid_stream_body()
    body["device_id"] = "x" * 65
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_device_id_invalid_chars(client):
    body = valid_stream_body()
    body["device_id"] = "device@invalid!"
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_live_type_invalid(client):
    body = valid_stream_body()
    body["live"] = "yes"
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_required_field(client):
    response = await client.post(
        "/api/v1/streams",
        json={"video_id": PUBLIC_VIDEO},
        headers=HEADERS_BASIC,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_path_traversal_refused(client):
    body = valid_stream_body(video_id="../../../etc/passwd")
    response = await client.post("/api/v1/streams", json=body, headers=HEADERS_BASIC)
    assert response.status_code == 422
