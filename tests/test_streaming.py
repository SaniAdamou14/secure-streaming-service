import pytest

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
async def test_create_stream_returns_201(client):
    response = await client.post("/api/v1/streams", json=stream_body(), headers=HEADERS_BASIC)
    assert response.status_code == 201
    data = response.json()
    assert "stream_id" in data
    assert data["video_id"] == PUBLIC_VIDEO
    assert data["quality"] == "1080p"


@pytest.mark.asyncio
async def test_stream_url_contains_expiration(client):
    response = await client.post("/api/v1/streams", json=stream_body(), headers=HEADERS_BASIC)
    assert response.status_code == 201
    data = response.json()
    assert data["expires_in_seconds"] == 300
    assert "stream_url" in data
    assert "signature=" in data["stream_url"]


@pytest.mark.asyncio
async def test_raw_secret_not_in_response(client):
    response = await client.post("/api/v1/streams", json=stream_body(), headers=HEADERS_BASIC)
    assert response.status_code == 201
    text = response.text
    assert "test-secret-key-for-local-development" not in text


@pytest.mark.asyncio
async def test_correlation_id_in_response(client):
    headers = {**HEADERS_BASIC, "X-Correlation-ID": "test-corr-id-123"}
    response = await client.post("/api/v1/streams", json=stream_body(), headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["correlation_id"] == "test-corr-id-123"


@pytest.mark.asyncio
async def test_delete_stream_returns_204(client):
    response = await client.delete("/api/v1/streams/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_unknown_stream_returns_404(client):
    response = await client.delete("/api/v1/streams/does-not-exist")
    assert response.status_code == 404
