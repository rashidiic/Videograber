from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.logging_config import get_logger

logger = get_logger(__name__)

HELP_TEXT = (
    "📹 Send me a video link from:\n"
    "• YouTube\n"
    "• Instagram\n"
    "• TikTok\n"
    "• Or any other video platform\n\n"
    "✨ I'll download it and extract the audio as MP3\n\n"
    "📌 <b>Example:</b>\n"
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 <b>Welcome to Audio Extractor!</b>\n\n"
        "🎵 I help you extract audio from videos and convert them to MP3\n\n"
        f"{HELP_TEXT}",
        parse_mode="HTML"
    )
    logger.info("User %s started the bot.", update.effective_user.id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "❓ <b>How to use:</b>\n\n"
        f"{HELP_TEXT}",
        parse_mode="HTML"
    )


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)


def register_start_handlers(app: Application) -> None:
    app.add_handler(start_handler)
    app.add_handler(help_handler)
