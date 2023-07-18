from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


upload = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Загрузить уведомления"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)