class StreamingError(Exception):
    pass


class ValidationFailure(StreamingError):
    def __init__(self, message: str = "Invalid request parameters."):
        self.message = message
        super().__init__(self.message)


class AuthenticationFailure(StreamingError):
    def __init__(self, message: str = "Authentication required."):
        self.message = message
        super().__init__(self.message)


class AuthorizationFailure(StreamingError):
    def __init__(self, message: str = "Access to this content is not permitted."):
        self.message = message
        super().__init__(self.message)


class ContentNotFound(StreamingError):
    def __init__(self, message: str = "Requested content not found."):
        self.message = message
        super().__init__(self.message)


class ContentUnavailable(StreamingError):
    def __init__(self, message: str = "Content is temporarily unavailable."):
        self.message = message
        super().__init__(self.message)


class CapacityExceeded(StreamingError):
    def __init__(self, retry_after: int = 5, message: str = "Service capacity exceeded."):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)


class DependencyTimeout(StreamingError):
    def __init__(self, message: str = "External dependency timed out."):
        self.message = message
        super().__init__(self.message)


class TemporaryDependencyFailure(StreamingError):
    def __init__(self, message: str = "External dependency temporarily unavailable."):
        self.message = message
        super().__init__(self.message)


class PermanentDependencyFailure(StreamingError):
    def __init__(self, message: str = "External dependency permanently unavailable."):
        self.message = message
        super().__init__(self.message)


HTTP_ERROR_MAP = {
    ValidationFailure: 422,
    AuthenticationFailure: 401,
    AuthorizationFailure: 403,
    ContentNotFound: 404,
    ContentUnavailable: 409,
    CapacityExceeded: 503,
    DependencyTimeout: 503,
    TemporaryDependencyFailure: 503,
    PermanentDependencyFailure: 502,
}
