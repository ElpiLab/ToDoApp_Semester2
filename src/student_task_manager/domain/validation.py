import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$")


def normalize_email(email: str) -> str:
    return email.strip().lower()


def is_valid_email(value: str) -> bool:
    return EMAIL_PATTERN.fullmatch(value) is not None
