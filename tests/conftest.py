import pytest
from httpx import ASGITransport, AsyncClient

from app.core.rate_limit import rate_limiter
from app.main import app
from app.routers.streaming import active_streams
from app.services.capacity_service import capacity_service


@pytest.fixture(autouse=True)
def reset_state():
    rate_limiter._requests.clear()
    capacity_service._active = 0
    active_streams.clear()
    yield
    rate_limiter._requests.clear()
    capacity_service._active = 0
    active_streams.clear()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
