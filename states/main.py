from aiogram.dispatcher.filters.state import StatesGroup, State


# Создаем группу состояний Order - для заказа.

class Main(StatesGroup):
    first = State()
    last = State()




