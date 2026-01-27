import re


def is_nonempty(value: str) -> bool:
    return bool(value and value.strip())


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_password(password: str) -> bool:
    return bool(password) and len(password) >= 6


def is_valid_phone(phone: str) -> bool:
    if not phone:
        return False
    # aceptar dígitos, espacios, + y -
    return bool(re.match(r"^[0-9\s\+\-]{7,15}$", phone))
