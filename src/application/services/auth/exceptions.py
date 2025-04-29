from typing import Optional

from fastapi import status, HTTPException


class NotTokenDataError(RuntimeError):

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "need to transfer 'token' or 'payload' from token for get user id"

        super().__init__(message)


TokenNotFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="token not found in the header",
)


NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="token is not valid",
)


TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="token has expired",
)


ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="no access rights",
)
