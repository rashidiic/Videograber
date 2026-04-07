from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.logging_config import get_logger

logger = get_logger(__name__)

HELP_TEXT = (
    "Send me a video link (YouTube, Instagram, TikTok, etc.), "
    "and I will download it, extract audio (MP3), and return the processing result.\n\n"
    "Example:\n"
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! I am a bot for extracting audio from video.\n\n"
        f"{HELP_TEXT}"
    )
    logger.info("User %s started the bot.", update.effective_user.id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)