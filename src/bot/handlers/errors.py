from telegram import Update
from telegram.ext import ContextTypes
from bot.logging_config import get_logger

logger = get_logger(__name__)


async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled exception: %s", context.error, exc_info=context.error)
    if isinstance(update, Update) and update.message is not None:
        try:
            await update.message.reply_text(
                "An unexpected error occurred. Please try again or send a different URL."
            )
        except Exception:
            logger.exception("Failed to send error message to user.")