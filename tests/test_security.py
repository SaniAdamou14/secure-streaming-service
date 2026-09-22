from app.core.logging import logger
from app.core.security import generate_signed_url, verify_signed_url


def test_raw_token_absent_from_logs(caplog):
    with caplog.at_level("INFO"):
        logger.info("test event")
    for record in caplog.records:
        assert "test-secret-key-for-local-development" not in record.getMessage()


def test_signed_url_generation():
    url = generate_signed_url(
        video_id="70fbf379-9c34-4ec4-9d07-a3ee75d794c2",
        user_id="user-basic",
        quality="1080p",
    )
    assert "signature=" in url
    assert "expires_at=" in url


def test_signed_url_verification():
    url = generate_signed_url(
        video_id="70fbf379-9c34-4ec4-9d07-a3ee75d794c2",
        user_id="user-basic",
        quality="1080p",
    )
    from urllib.parse import parse_qs, urlparse

    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    assert verify_signed_url(
        video_id=params["video_id"][0],
        user_id=params["user_id"][0],
        quality=params["quality"][0],
        expires_at=int(params["expires_at"][0]),
        signature=params["signature"][0],
    )


def test_invalid_signature_rejected():
    result = verify_signed_url(
        video_id="70fbf379-9c34-4ec4-9d07-a3ee75d794c2",
        user_id="user-basic",
        quality="1080p",
        expires_at=9999999999,
        signature="invalid-signature",
    )
    assert result is False


def test_expired_signature_rejected():
    result = verify_signed_url(
        video_id="70fbf379-9c34-4ec4-9d07-a3ee75d794c2",
        user_id="user-basic",
        quality="1080p",
        expires_at=1000000000,
        signature="does-not-matter",
    )
    assert result is False
