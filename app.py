import asyncio
import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot import bot, dp, scheduler, setup_webhook, remove_webhook, init_db, notify_all_users, process_recurring_payments

# ---------- Настройки ----------
PORT = int(os.environ.get("PORT", 10000))
# Render даёт URL сервиса в этой переменной окружения
APP_URL = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:10000")


# ---------- Фоновая задача для планировщика ----------
async def on_startup(app: web.Application):
    """Что делать при старте приложения."""
    init_db()

    # Регистрируем вебхук в Telegram
    await setup_webhook(APP_URL)

    # Запускаем планировщик (напоминания и регулярные платежи)
    scheduler.add_job(notify_all_users, "interval", minutes=1, id="notify_check")
    scheduler.add_job(process_recurring_payments, "interval", minutes=30, id="recurring_check")
    scheduler.start()

    print("Бот и планировщик запущены.")


async def on_shutdown(app: web.Application):
    """Что делать при остановке приложения."""
    await remove_webhook()
    scheduler.shutdown()


def main():
    # Создаём aiohttp-приложение
    app = web.Application()

    # Регистрируем обработчики старта и остановки
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # --- Настройка Webhook для aiogram ---
    # Все запросы на /webhook будут передаваться в dispatcher aiogram
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")

    # Настраиваем приложение (внутренние хуки aiogram)
    setup_application(app, dp, bot=bot)

    # --- Health-check для Render ---
    async def health(request):
        return web.Response(text="OK")

    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    # --- Запуск ---
    web.run_app(app, host="0.0.0.0", port=PORT)
    print(f"Сервер запущен на порту {PORT}")


if __name__ == "__main__":
    main()