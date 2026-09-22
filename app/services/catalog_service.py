from enum import Enum


class AccessLevel(str, Enum):  # noqa: UP042
    PUBLIC = "public"
    PREMIUM = "premium"
    OWNER_ONLY = "owner-only"


class VideoEntry:
    def __init__(
        self,
        video_id: str,
        title: str,
        access: AccessLevel,
        qualities: list[str],
        live: bool = False,
        owner: str = "",
    ):
        self.video_id = video_id
        self.title = title
        self.access = access
        self.qualities = qualities
        self.live = live
        self.owner = owner


CATALOG: dict[str, VideoEntry] = {
    "70fbf379-9c34-4ec4-9d07-a3ee75d794c2": VideoEntry(
        video_id="70fbf379-9c34-4ec4-9d07-a3ee75d794c2",
        title="Public Documentary",
        access=AccessLevel.PUBLIC,
        qualities=["360p", "480p", "720p", "1080p"],
    ),
    "550e8400-e29b-41d4-a716-446655440000": VideoEntry(
        video_id="550e8400-e29b-41d4-a716-446655440000",
        title="Premium Series",
        access=AccessLevel.PREMIUM,
        qualities=["720p", "1080p"],
    ),
    "4ad353d0-fab8-4eb4-9989-ab1f25ab9a00": VideoEntry(
        video_id="4ad353d0-fab8-4eb4-9989-ab1f25ab9a00",
        title="Private Upload",
        access=AccessLevel.OWNER_ONLY,
        qualities=["480p", "720p"],
        owner="user-owner",
    ),
    "e76ea484-5f96-4bf2-927d-763114eae4ce": VideoEntry(
        video_id="e76ea484-5f96-4bf2-927d-763114eae4ce",
        title="Live News",
        access=AccessLevel.PREMIUM,
        qualities=["480p", "720p"],
        live=True,
    ),
}


def get_video(video_id: str) -> VideoEntry | None:
    return CATALOG.get(video_id)


def get_all_video_ids() -> list[str]:
    return list(CATALOG.keys())
