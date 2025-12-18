import re


def is_valid_android_id(string: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{16}", string))
