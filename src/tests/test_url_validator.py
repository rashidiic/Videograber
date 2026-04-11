from utils.url_validator import extract_url, is_valid_url


class TestExtractUrl:
    def test_simple_url(self) -> None:
        assert extract_url("Check this: https://example.com/video") == "https://example.com/video"

    def test_no_url(self) -> None:
        assert extract_url("Just plain text here") is None

    def test_youtube_url(self) -> None:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_url(f"Look {url} now") == url

    def test_http_url(self) -> None:
        assert extract_url("http://example.com") == "http://example.com"

    def test_empty_string(self) -> None:
        assert extract_url("") is None

    def test_url_with_query_params(self) -> None:
        url = "https://example.com/path?a=1&b=2"
        assert extract_url(url) == url


class TestIsValidUrl:
    def test_valid_https(self) -> None:
        assert is_valid_url("https://example.com") is True

    def test_valid_http(self) -> None:
        assert is_valid_url("http://example.com") is True

    def test_no_scheme(self) -> None:
        assert is_valid_url("example.com") is False

    def test_ftp_scheme(self) -> None:
        assert is_valid_url("ftp://example.com") is False

    def test_empty_string(self) -> None:
        assert is_valid_url("") is False

    def test_just_scheme(self) -> None:
        assert is_valid_url("https://") is False
