from pathlib import Path

import httpx

from bot.logging_config import get_logger
from services.mock_data import get_mock_response

logger = get_logger(__name__)


class DummyApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def upload_mp3(self, file_path: Path) -> dict:
        logger.info("Uploading %s to %s", file_path.name, self.base_url)
        async with httpx.AsyncClient(timeout=120) as client:
            try:
                with file_path.open("rb") as f:
                    await client.post(
                        self.base_url,
                        files={"file": (file_path.name, f, "audio/mpeg")},
                    )
                logger.info("Upload completed (response ignored).")
            except httpx.HTTPError as exc:
                logger.warning("HTTP error during upload (non-fatal): %s", exc)
        return get_mock_response(file_path.name)
