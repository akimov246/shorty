import base62
import secrets
from string import digits, ascii_lowercase, ascii_uppercase

CHARSET = digits + ascii_lowercase + ascii_uppercase
LENGTH_OF_RANDOM_STRING = 7

def generate_short_code(id: int) -> str:
    base = base62.encode(id)
    random_string = "".join(secrets.choice(CHARSET) for _ in range(LENGTH_OF_RANDOM_STRING))
    short_code = base + random_string
    return short_code