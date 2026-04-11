from pathlib import Path

from bot.logging_config import get_logger

logger = get_logger(__name__)


class TemporaryFileManager:
    def __init__(self, tmp_dir: Path) -> None:
        self._tmp_dir = tmp_dir
        self._files: set[Path] = set()

    def register(self, path: Path) -> None:
        self._files.add(path)

    def cleanup(self) -> None:
        for path in self._files:
            try:
                if path.exists():
                    path.unlink()
                    logger.debug("Deleted temp file: %s", path)
            except OSError as exc:
                logger.warning("Could not delete %s: %s", path, exc)
        self._files.clear()
