from typing import Literal

from pydantic import BaseModel


class TokenFormResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str
