import secrets
import re


def generate_unique_random_string(length=10):
    """Generate random string."""
    random_string = secrets.token_urlsafe(length)[:length]
    return random_string


def remove_special_character(strng: str):
    """Remove all special caractere of strng."""
    formated = re.sub(r'[|/.\-]', '', strng)
    return formated
