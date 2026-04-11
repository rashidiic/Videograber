import asyncio
from pathlib import Path

from yt_dlp import YoutubeDL

from bot.logging_config import get_logger

logger = get_logger(__name__)

_YDL_OPTS: dict = {
    "format": "bestaudio/best",
    "outtmpl": "%(id)s.%(ext)s",
    "quiet": True,
    "no_warnings": True,
}


async def download_video(url: str, output_dir: Path) -> Path:
    opts = {**_YDL_OPTS, "outtmpl": str(output_dir / "%(id)s.%(ext)s")}
    loop = asyncio.get_running_loop()

    def _download() -> str:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise RuntimeError(f"yt-dlp returned no info for {url}")
            filename = ydl.prepare_filename(info)
            return filename

    filepath = await loop.run_in_executor(None, _download)
    result = Path(filepath)
    if not result.exists():
        raise FileNotFoundError(f"Downloaded file not found: {result}")
    logger.info("Downloaded: %s (%s)", result.name, _human_size(result.stat().st_size))
    return result


def _human_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"
