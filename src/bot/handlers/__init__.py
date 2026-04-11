from telegram.ext import Application

from bot.handlers.start import register_start_handlers
from bot.handlers.url_handler import URLHandler


def register_all_handlers(app: Application) -> None:
    register_start_handlers(app)
    app.add_handler(URLHandler())
