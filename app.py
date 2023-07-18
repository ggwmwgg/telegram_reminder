import asyncio

from aiogram import executor
from tortoise import Tortoise

from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.dp_api import init_db, check_notifications
import middlewares, handlers  # Не удалять, влияет на работу бота.

async def on_startup(dp):
    # Устанавливаем связь с бд, уведомляем админов и устанавливаем команды.

    await init_db()
    await on_startup_notify(dp)
    await set_default_commands(dp)
    asyncio.create_task(check_notifications(dp))

async def on_shutdown(dp):
    # Закрываем соединение с бд.
    await Tortoise.close_connections()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
