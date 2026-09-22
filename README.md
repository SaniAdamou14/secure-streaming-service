# Secure Streaming Service

A defensive, secure Python API that authorizes video streaming sessions.

## Architecture

```
app/
  main.py              - FastAPI application entry point
  config.py            - Environment-based configuration
  middleware.py         - Correlation ID middleware
  core/
    exceptions.py      - Custom exceptions with HTTP mapping
    logging.py         - Structured JSON logging
    security.py        - HMAC-SHA256 signed URLs
    rate_limit.py      - Per-user rate limiting
    retry.py           - Exponential backoff with jitter
  services/
    auth_service.py    - User authentication and authorization
    catalog_service.py - Synthetic video catalog
    capacity_service.py- Stream capacity management
    recommendation_service.py - External recommendation fetcher
    streaming_service.py - Core streaming logic
  routers/
    health.py          - Health and readiness endpoints
    streaming.py       - Stream creation and deletion
```

## Prerequisites

- Python 3.12+
- Docker (optional)

## Installation

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STREAM_TOKEN_SECRET` | (required) | HMAC secret for signed URLs |
| `PREVIOUS_STREAM_TOKEN_SECRET` | | Previous secret for rotation |
| `MAX_ACTIVE_STREAMS` | 100 | Maximum concurrent streams |
| `RATE_LIMIT_REQUESTS` | 5 | Requests per window |
| `RATE_LIMIT_WINDOW_SECONDS` | 60 | Rate limit window |

## Running Locally

```bash
uvicorn app.main:app --reload
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |
| POST | `/api/v1/streams` | Create a streaming session |
| DELETE | `/api/v1/streams/{stream_id}` | End a streaming session |

## Tests

```bash
pytest -q --cov=app --cov-report=term-missing
```

## Security Scans

```bash
ruff format --check .
ruff check .
bandit -r app
semgrep scan --config p/python app tests
gitleaks dir .
trivy fs --scanners vuln,secret,misconfig .
```

## Docker

```bash
docker build -t secure-streaming-service .
docker run --rm -p 8000:8000 -e STREAM_TOKEN_SECRET=your-secret secure-streaming-service
```

## Limitations

- No real video delivery
- In-memory catalog only
- Synthetic user data
- Not a CDN or DRM solution
- No real database
