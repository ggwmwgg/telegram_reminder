import asyncio
import logging
from aiogram import types
from datetime import datetime, timezone
from tortoise import Tortoise
from data.config import POSTGRES_URI
from utils.db_api.models import User, Notification


# Инициализация БД
async def init_db():
    logging.info("Подключение к БД...")
    await Tortoise.init(
        db_url=POSTGRES_URI,
        modules={'models': ['utils.db_api.models']}
    )
    # Добавляем таблицы в БД
    await Tortoise.generate_schemas()


async def check_notifications(dp):
    while True:
        # Получаем список 5 последних уведомлений по дате
        notifications = await Notification.filter(is_sent=False).order_by('-send_at').limit(5)
        current_time = datetime.now().replace(tzinfo=timezone.utc)
        time_format = "%d.%m.%Y %H:%M"
        for notification in notifications:
            if notification.send_at <= current_time:
                answer_time = notification.answer_time * 60
                username = await User.get_or_none(tg_id=notification.user_id)
                yes_no = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
                yes_no.add(types.InlineKeyboardButton("Выполнено", callback_data=f"yes:{notification.id}"),
                           types.InlineKeyboardButton("Не сделано", callback_data=f"no:{notification.id}"))
                text_to_adm = f"Отправляем уведомление от {notification.send_at.strftime(time_format)} пользователю {username.username}"
                text_to_usr = f"{notification.text}\n\nПодтвердите выполнение."

                await dp.bot.send_message(notification.admin_id, text_to_adm)
                message = await dp.bot.send_message(notification.user_id, text_to_usr, reply_markup=yes_no)
                asyncio.create_task(remove_keyboard(dp, message.chat.id, message.message_id, answer_time, notification.id))
                notification.is_sent = True
                await notification.save()
        await asyncio.sleep(10)


async def remove_keyboard(dp, chat_id, message_id, answer_time, notification_id):
    await asyncio.sleep(answer_time)
    notification = await Notification.get_or_none(id=notification_id)
    time_format = "%d.%m.%Y %H:%M"
    if notification.expired:
        return
    else:
        user = await User.get_or_none(tg_id=notification.user_id)
        text_to_usr = notification.text + "\n\nСрок истек."
        text_to_adm = f"Срок уведомления от {notification.send_at.strftime(time_format)} истек.\nПользователь {user.username} не подтвердил выполнение"
        notification.expired = True

        await dp.bot.edit_message_text(
            text=text_to_usr,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None
        )
        await dp.bot.send_message(notification.admin_id, text_to_adm)
    await notification.delete()
