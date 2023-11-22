import re


def validate_phone_number(phone_number):
    regex_pattern = r'^\+\d+$'
    match = re.match(regex_pattern, phone_number)
    return bool(match)



def validate_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email))
