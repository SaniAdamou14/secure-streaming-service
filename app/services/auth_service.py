from enum import Enum


class Role(str, Enum):  # noqa: UP042
    BASIC = "basic"
    PREMIUM = "premium"
    OWNER = "owner"
    ADMIN = "admin"


class User:
    def __init__(self, user_id: str, role: Role):
        self.user_id = user_id
        self.role = role


USERS = {
    "user-basic": User(user_id="user-basic", role=Role.BASIC),
    "user-premium": User(user_id="user-premium", role=Role.PREMIUM),
    "user-owner": User(user_id="user-owner", role=Role.OWNER),
    "user-admin": User(user_id="user-admin", role=Role.ADMIN),
}

TOKENS = {
    "test-basic-token": "user-basic",
    "test-premium-token": "user-premium",
    "test-owner-token": "user-owner",
    "test-admin-token": "user-admin",
}


def authenticate_user(token: str) -> User | None:
    user_id = TOKENS.get(token)
    if user_id is None:
        return None
    return USERS.get(user_id)


def check_authorization(user: User, video_entry, requested_quality: str) -> bool:
    from app.services.catalog_service import AccessLevel

    if requested_quality not in video_entry.qualities:
        return False

    if video_entry.access == AccessLevel.PUBLIC:
        return True

    if video_entry.access == AccessLevel.PREMIUM:
        return user.role in (Role.PREMIUM, Role.ADMIN)

    if video_entry.access == AccessLevel.OWNER_ONLY:
        return user.user_id == video_entry.owner or user.role == Role.ADMIN

    return False
