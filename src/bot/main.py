from telegram import BotCommand
from telegram.ext import ApplicationBuilder

from bot.config import get_settings
from bot.handlers import register_all_handlers
from bot.handlers.errors import global_error_handler
from bot.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


async def setup_menu_commands(app) -> None:
    """Set up bot menu commands with descriptions."""
    commands = [
        BotCommand("start", "Start the bot and get help"),
        BotCommand("help", "Show help information"),
    ]
    await app.bot.set_my_commands(commands)
    logger.info("Menu commands set up successfully")


def main() -> None:
    settings = get_settings()
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

    # Set up menu commands
    app.post_init = setup_menu_commands

    logger.info("Bot is running. Press Ctrl-C to stop.")
    app.run_polling()
