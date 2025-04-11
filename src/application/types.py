from enum import Enum


class StationStatusType(str, Enum):
    NOT_VERIFIED = "not_verified"
    NOT_WORK = "not_work"
    WORKS = "works"
