import asyncio
import subprocess
from pathlib import Path
from bot.logging_config import get_logger

logger = get_logger(__name__)


async def convert_to_mp3(video_path: Path, output_dir: Path) -> Path:
    mp3_path = output_dir / (video_path.stem + ".mp3")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn", "-acodec", "libmp3lame",
        "-ab", "192k", "-ar", "44100", "-ac", "2",
        str(mp3_path),
    ]
    loop = asyncio.get_running_loop()

    def _run() -> None:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stderr:
            logger.debug("ffmpeg stderr: %s", result.stderr[:500])

    await loop.run_in_executor(None, _run)
    if not mp3_path.exists():
        raise FileNotFoundError(f"MP3 conversion produced no output: {mp3_path}")
    logger.info("Converted to MP3: %s", mp3_path.name)
    return mp3_path