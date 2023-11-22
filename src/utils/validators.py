import re


def validate_phone(phone):
    padrao = r"^\+\d{2}\d{10}$"
    return bool(re.match(padrao, phone))


def validate_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email))
