from pathlib import Path
from unittest.mock import AsyncMock, patch
import httpx
from bot.services.api_client import DummyApiClient


class TestDummyApiClient:
    async def test_upload_returns_mock_data(self, tmp_path: Path) -> None:
        mp3_file = tmp_path / "test.mp3"
        mp3_file.write_bytes(b"\x00" * 100)
        client = DummyApiClient.__new__(DummyApiClient)
        client.base_url = "https://httpbin.org/post"
        mock_post = AsyncMock()
        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_cm)
        mock_cm.__aexit__ = AsyncMock(return_value=False)
        mock_cm.post = mock_post
        with patch("bot.services.api_client.httpx.AsyncClient", return_value=mock_cm):
            result = await client.upload_mp3(mp3_file)
        assert isinstance(result, dict)
        assert result["status"] == "ok"
        assert result["filename"] == "test.mp3"
        assert "transcription" in result
        assert "duration_seconds" in result

    async def test_upload_handles_http_error(self, tmp_path: Path) -> None:
        mp3_file = tmp_path / "test.mp3"
        mp3_file.write_bytes(b"\x00" * 100)
        client = DummyApiClient.__new__(DummyApiClient)
        client.base_url = "https://httpbin.org/post"
        mock_post = AsyncMock(side_effect=httpx.HTTPError("Server error"))
        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_cm)
        mock_cm.__aexit__ = AsyncMock(return_value=False)
        mock_cm.post = mock_post
        with patch("bot.services.api_client.httpx.AsyncClient", return_value=mock_cm):
            result = await client.upload_mp3(mp3_file)
        assert result["status"] == "ok"