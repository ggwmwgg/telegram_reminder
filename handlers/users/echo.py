from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loader import dp


# Обработка неизвестных команд
@dp.message_handler()
async def bot_echo(message: types.Message, state: FSMContext):
    text = "Неизвестная команда\nНажмите /start для перезапуска"
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await state.finish()


