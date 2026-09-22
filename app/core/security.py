import hashlib
import hmac
import time
from urllib.parse import urlencode

from app.config import settings


def generate_signed_url(video_id: str, user_id: str, quality: str) -> str:
    expires_at = int(time.time()) + 300
    payload = {
        "video_id": video_id,
        "user_id": user_id,
        "quality": quality,
        "expires_at": expires_at,
    }
    sorted_params = urlencode(sorted(payload.items()))
    signature = hmac.new(
        settings.stream_token_secret.encode("utf-8"),
        sorted_params.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    signed_params = {**payload, "signature": signature}
    query = urlencode(sorted(signed_params.items()))
    return f"https://cdn.example.test/stream/{video_id}?{query}"


def verify_signed_url(
    video_id: str, user_id: str, quality: str, expires_at: int, signature: str
) -> bool:
    now = int(time.time())
    if expires_at < now:
        return False

    payload = {
        "video_id": video_id,
        "user_id": user_id,
        "quality": quality,
        "expires_at": expires_at,
    }
    sorted_params = urlencode(sorted(payload.items()))

    current_sig = hmac.new(
        settings.stream_token_secret.encode("utf-8"),
        sorted_params.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if hmac.compare_digest(current_sig, signature):
        return True

    if settings.previous_stream_token_secret:
        prev_sig = hmac.new(
            settings.previous_stream_token_secret.encode("utf-8"),
            sorted_params.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(prev_sig, signature)

    return False
