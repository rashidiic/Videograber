import re
from urllib.parse import urlparse

_URL_PATTERN = re.compile(
    r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\-._~:?#@!$&'()*+,;=%]*",
    re.IGNORECASE,
)


def extract_url(text: str) -> str | None:
    match = _URL_PATTERN.search(text.strip())
    return match.group(0) if match else None


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False
