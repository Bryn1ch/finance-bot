import asyncio
import os
import threading
from flask import Flask

from bot import main


flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return "Bot is running", 200


@flask_app.route("/health")
def health():
    return "OK", 200


def run_bot():
    """Запускает бота в отдельном потоке с собственным event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


if __name__ == "__main__":
    # Запускаем бота в фоновом потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Flask слушает порт, который даёт Render
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)