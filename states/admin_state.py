from aiogram.filters.state import State, StatesGroup


# Создаем класс для группы состояний админа нашей FSM
class FSMadmin(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_enter_date = State() # Состояние ожидания ввода даты