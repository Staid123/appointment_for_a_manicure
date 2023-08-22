from aiogram.filters.state import State, StatesGroup


# Создаем класс для группы состояний админа нашей FSM
class FSMadmin(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_yes_no_in_start = State() # Состояние ожидания ответа на команду старт
    fill_enter_client_name = State() # Состояние ожидания ввода имени клиента
    fill_enter_client_phone_number = State() # Состояние ожидания ввода номера телефона клиента
    fill_enter_year = State() # Состояние ожидания ввода года
    fill_enter_month = State() # Состояние ожидания ввода месяца
    fill_enter_working_date = State() # Состояние ожидания ввода даты
    fill_enter_working_time = State() # Состояние ожидания ввода времени
    fill_enter_type_of_service = State() # Состояние ожидания ввода типа услуги
    fill_edit_working_time = State() # Состояние ожидания изменения даты записи