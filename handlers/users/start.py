from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import upload
from loader import dp
from states.main import Main
from utils import get_data
from utils.db_api.models import User, Notification
from utils.misc import rate_limit


# Обработка команды /start
@rate_limit(5, key="start")
@dp.message_handler(CommandStart(), state='*')  # state=None
async def bot_start(message: types.Message):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user is None:
        await User.create(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        user_info = f"Регистрация успешна!\nID: {message.from_user.id}\nUsername: @{message.from_user.username}\nИмя: {message.from_user.full_name}"
        await message.answer(user_info, reply_markup=ReplyKeyboardRemove())
    elif user.is_manager is False:
        user_info = f"Инфо\nID: {message.from_user.id}\nUsername: @{message.from_user.username}\nИмя: {message.from_user.full_name}"
        await message.answer(user_info, reply_markup=ReplyKeyboardRemove())
    elif user.is_manager is True:
        user_info = f"Инфо | Менеджер\nID: {message.from_user.id}\nUsername: @{message.from_user.username}\nИмя: {message.from_user.full_name}\nВы являетесь менеджером"
        await message.answer(user_info, reply_markup=upload)

    await Main.first.set()


# Обработка показа кнопки загрузки менеджеру
@rate_limit(2, key="main_manager")
@dp.message_handler(Text(equals=["Загрузить уведомления"]), state="*")
async def msg_main(message: types.Message, state: FSMContext):
    user = await User.get_or_none(tg_id=message.from_user.id)
    if user is None or user.is_manager is False:
        await message.answer("У вас нет доступа к этой команде")
    else:
        await message.answer("Введите ссылку листа из Google Sheets.", reply_markup=ReplyKeyboardRemove())
        await Main.last.set()

# Обработка загрузки списка уведомлений
@rate_limit(2, key="main_manager_upload")
@dp.message_handler(Text, state=Main.last)
async def msg_main_link(message: types.Message, state: FSMContext):
    msg = message.text
    datetime_format = "%d.%m.%Y %H:%M"
    if "https://docs.google.com/spreadsheets/d/" in msg:
        sheet_id = msg.split("https://docs.google.com/spreadsheets/d/")[1].split("/")[0]
        new_data = get_data(sheet_id)
        for i in new_data:
            datetime_str = i['date'] + " " + i['time']
            datetime_new = datetime.strptime(datetime_str, datetime_format)
            await Notification.create(
                user_id=i['tg_id'],
                admin_id=message.from_user.id,
                text=i['text'],
                send_at=datetime_new,
                answer_time=i['answer_time']
            )
        await message.answer("Уведомления успешно загружены.", reply_markup=upload)
        await Main.first.set()
    else:
        await message.answer("Неверная ссылка. Попробуйте еще раз.")


# Обработка ответов на уведомления
@rate_limit(2, key="main_callback")
@dp.callback_query_handler(lambda cb: cb.data.startswith('yes') or cb.data.startswith('no'), state="*")
async def callback_main(query: types.CallbackQuery, state: FSMContext):
    call, notification_id = query.data.split(":")

    notification = await Notification.get_or_none(id=notification_id)
    time_format = "%d.%m.%Y %H:%M"
    text_to_usr = ""
    text_to_adm = ""
    if notification is None or notification.expired:
        await query.answer(f"Уведомление не найдено или срок уведомления истек")
    if call == "yes":
        text_to_usr = notification.text + "\n\nВы подтвердили выполнение."
        text_to_adm = f"Пользователь @{query.from_user.username} подтвердил выполнение уведомления от {notification.send_at.strftime(time_format)}"
    elif call == "no":
        text_to_usr = notification.text + "\n\nВы отклонили выполнение."
        text_to_adm = f"Пользователь @{query.from_user.username} отклонил выполнение уведомления от {notification.send_at.strftime(time_format)}"

    notification.expired = True
    await notification.save()
    await dp.bot.edit_message_text(
        text=text_to_usr,
        chat_id=notification.user_id,
        message_id=query.message.message_id,
        reply_markup=None
    )
    await dp.bot.send_message(
        text=text_to_adm,
        chat_id=notification.admin_id
    )









