from enum import Enum


class StationStatusType(str, Enum):
    NOT_VERIFIED = "not_verified"
    NOT_WORK = "not_work"
    WORKS = "works"


class CheckerType(str, Enum):
    FFPLAY = "ffplay"
    FFPROBE = "ffprobe"
    VLC = "vlc"


class UserAccessRights(str, Enum):
    DEFAULT = "default"
    PLUS = "plus"
    PRO = "pro"
    FULL = "full"
    OWNER = "owner"


class FilePlaylistType(str, Enum):
    M3U = "m3u"
    PLS = "pls"
    JSON = "json"
