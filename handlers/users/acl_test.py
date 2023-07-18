from aiogram import types
from aiogram.dispatcher.filters import Command
from data.config import admins
from loader import dp
from utils.db_api.models import User


# Добавление менеджера будучи админом
@dp.message_handler(Command("m_add"), state="*")
async def manager_add(message: types.Message):
    args = message.get_args()
    if message.from_user.id in admins:
        if args.isdigit():
            user = await User.get_or_none(tg_id=int(args))
            if user is None:
                await message.answer("Пользователь не найден")
            else:
                user.is_manager = True
                await user.save()
                await message.answer(f"Пользователь имеет статус: {user.is_manager}. Теперь он менеджер.")
        else:
            await message.answer("Введите ID пользователя")
    else:
        await message.answer("У вас нет доступа к этой команде")
