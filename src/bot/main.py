from telegram.ext import ApplicationBuilder

from bot.config import Settings
from bot.handlers import register_all_handlers
from bot.handlers.errors import global_error_handler
from bot.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def main() -> None:
    settings = Settings()
    setup_logging(settings.log_level)
    logger.info("Starting bot…")
    settings.tmp_dir.mkdir(parents=True, exist_ok=True)

    app = (
        ApplicationBuilder()
        .token(settings.telegram_token)
        .concurrent_updates(True)
        .build()
    )
    register_all_handlers(app)
    app.add_error_handler(global_error_handler)
    logger.info("Bot is running. Press Ctrl-C to stop.")
    app.run_polling()