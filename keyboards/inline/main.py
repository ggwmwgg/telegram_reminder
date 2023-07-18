from aiogram import types


yes_no = types.InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
yes_no.add(types.InlineKeyboardButton("Выполнено", callback_data='yes'),
           types.InlineKeyboardButton("Не сделано", callback_data='no'))
