import asyncio
import subprocess
from pathlib import Path

from bot.logging_config import get_logger

logger = get_logger(__name__)


async def convert_to_mp3(video_path: Path, output_dir: Path) -> Path:
    mp3_path = output_dir / (video_path.stem + ".mp3")
    if video_path.suffix.lower() == ".mp3" and video_path == mp3_path:
        logger.info("Skipping conversion because input is already MP3: %s", video_path.name)
        return video_path

    tmp_mp3_path = output_dir / f"{video_path.stem}.converted.mp3"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn", "-acodec", "libmp3lame",
        "-ab", "192k", "-ar", "44100", "-ac", "2",
        str(tmp_mp3_path),
    ]
    loop = asyncio.get_running_loop()

    def _run() -> None:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stderr:
            logger.debug("ffmpeg stderr: %s", result.stderr[:500])
        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            raise RuntimeError(
                "ffmpeg failed to convert audio"
                + (f": {stderr[-500:]}" if stderr else "")
            )

    await loop.run_in_executor(None, _run)
    tmp_mp3_path.replace(mp3_path)
    if not mp3_path.exists():
        raise FileNotFoundError(f"MP3 conversion produced no output: {mp3_path}")
    logger.info("Converted to MP3: %s", mp3_path.name)
    return mp3_path
