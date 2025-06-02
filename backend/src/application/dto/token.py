from dataclasses import dataclass


@dataclass(slots=True)
class AccessToken:
    value: str
