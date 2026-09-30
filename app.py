import asyncio
import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot import (
    bot, dp, scheduler,
    setup_webhook, remove_webhook,
    init_db, notify_all_users, process_recurring_payments
)


PORT = int(os.environ.get("PORT", 10000))
APP_URL = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:10000")


async def on_startup(app: web.Application):
    init_db()
    await setup_webhook(APP_URL)
    scheduler.add_job(notify_all_users, "interval", minutes=1, id="notify_check")
    scheduler.add_job(process_recurring_payments, "interval", minutes=30, id="recurring_check")
    scheduler.start()
    print("Бот и планировщик запущены.")


async def on_shutdown(app: web.Application):
    await remove_webhook()
    scheduler.shutdown()


def main():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    async def health(request):
        return web.Response(text="OK")

    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()