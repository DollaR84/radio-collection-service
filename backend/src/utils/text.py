import re


def paschal_case_to_snake_case(string: str) -> str:
    return "_".join([word.lower() for word in re.findall(r"[A-Z][a-z0-9]+", string)])


def paschal_case_to_words(string: str) -> str:
    return " ".join(list(re.findall(r"[A-Z][a-z0-9]+", string)))
