from typing import Optional


class RemoveBGVideoError(Exception):
    """Base SDK error."""


class ApiError(RemoveBGVideoError):
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        request_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.request_id = request_id
