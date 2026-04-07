from telegram.ext import Application
from bot.handlers.start import start_handler
from bot.handlers.url_handler import URLHandler


def register_all_handlers(app: Application) -> None:
    app.add_handler(start_handler)
    app.add_handler(URLHandler())