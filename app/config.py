from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    stream_token_secret: str = "default-dev-secret"
    previous_stream_token_secret: str = ""
    max_active_streams: int = 100
    rate_limit_requests: int = 5
    rate_limit_window_seconds: int = 60
    recommendation_timeout_seconds: float = 1.5
    max_retry_attempts: int = 3

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
