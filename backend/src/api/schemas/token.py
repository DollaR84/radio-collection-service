from typing import Literal

from pydantic import BaseModel


class TokenFormResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class AccessTokenResponse(BaseModel):
    access_token: str
