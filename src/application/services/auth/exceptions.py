from typing import Optional

from fastapi import status, HTTPException


class NotTokenDataError(RuntimeError):

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "need to transfer 'token' or 'payload' from token for get user id"

        super().__init__(message)


class TokenNotFound(HTTPException):

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="token not found in the header",
        )


class NoJwtException(HTTPException):

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token is not valid",
        )


class TokenExpiredException(HTTPException):

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token has expired",
        )


class ForbiddenException(HTTPException):

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no access rights",
        )
