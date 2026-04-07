from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from bot.config import Settings
from bot.handlers.start import HELP_TEXT
from bot.logging_config import get_logger
from services.api_client import DummyApiClient
from services.converter import convert_to_mp3
from services.downloader import download_video
from utils.file_utils import TemporaryFileManager
from utils.formatters import format_response
from utils.url_validator import extract_url, is_valid_url

logger = get_logger(__name__)


class URLHandler(MessageHandler):
    def __init__(self) -> None:
        super().__init__(filters.TEXT & ~filters.COMMAND, self._handle_message)

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text or ""
        url = extract_url(text)

        if not url:
            await update.message.reply_text(
                "I could not find a link in your message.\n\n" f"{HELP_TEXT}"
            )
            return

        if not is_valid_url(url):
            await update.message.reply_text(
                f"This does not look like a valid link:\n{url}\n\n"
                "Please send a URL that starts with http:// or https://."
            )
            return

        settings = Settings()
        await update.message.reply_text(f"Got it! Downloading video from:\n{url}")
        logger.info("Processing URL from user %s: %s", update.effective_user.id, url)

        tmp_file_manager = TemporaryFileManager(settings.tmp_dir)
        try:
            video_path: Path | None = None
            try:
                video_path = await download_video(url, settings.tmp_dir)
                await update.message.reply_text("Video downloaded. Converting to MP3...")
            except Exception as exc:
                logger.exception("Download failed for %s", url)
                await update.message.reply_text(f"Failed to download the video.\nReason: {exc}")
                return

            mp3_path: Path | None = None
            try:
                mp3_path = await convert_to_mp3(video_path, settings.tmp_dir)
                await update.message.reply_text("Audio is ready! Sending it for processing...")
            except Exception as exc:
                logger.exception("Conversion failed for %s", video_path)
                await update.message.reply_text(
                    f"Failed to convert video to MP3.\nReason: {exc}"
                )
                return

            api_client = DummyApiClient(settings.dummy_api_url)
            try:
                result = await api_client.upload_mp3(mp3_path)
            except Exception as exc:
                logger.exception("API upload failed for %s", mp3_path)
                await update.message.reply_text(
                    f"Error while sending data to the server.\nReason: {exc}"
                )
                return

            reply = format_response(result)
            await update.message.reply_text(reply)
        finally:
            tmp_file_manager.cleanup()