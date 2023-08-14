from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import months, days_of_the_week, backward_forward
from services.file_handling import day_in_months


def yes_no_keyboard() -> InlineKeyboardMarkup:
    # Создаем кнопки Да и Нет
    yes_button: InlineKeyboardButton = InlineKeyboardButton(text='Да',
                                                            callback_data='yes_button_press')
    no_button: InlineKeyboardButton = InlineKeyboardButton(text='Нет',
                                                           callback_data='no_button_press')
    # Создаем объект клавиатуру с кнопками
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button]]
    # Создаем объект инлайн-клавиатуры
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


def enter_month_keyboard() -> InlineKeyboardMarkup:
    # Создаем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=month,
        callback_data=f'{num}') for num, month in months.items()], width=3)
    # Добавляем в билдер кнопкy отмены
    kb_builder.row(InlineKeyboardButton(
                            text='Отмена',
                            callback_data='cancel_button_press'))
                                        
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def enter_date_working_keyboard(year, month):
    # Создаем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем месяц первой кнопкой в билдер
    kb_builder.row(InlineKeyboardButton(
        text=f'{months[int(month)]} {year}',
        callback_data=f'{months[int(month)]}_button_press'))
    
    # Добавляем кнопки дни недели в билдер
    kb_builder.row(*[InlineKeyboardButton(
        text=day,
        callback_data=f'{day}_button_press') for day in days_of_the_week])
    
    # Получаем список с днями месяца
    lst_dates = day_in_months(year, month)
    # Добавляем дни месяца в билдер(5 рядов по 7 кнопок в каждом)
    kb_builder.row(*[InlineKeyboardButton(
        text=dat,
        callback_data=f'{dat}date') for dat in lst_dates], width=7)

    # Добавляем кнопки назад и вперед в билдер
    kb_builder.row(*[InlineKeyboardButton(
        text=button,
        callback_data=txt) for button, txt in backward_forward.items()])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def enter_time_working_keyboard(list_with_time, is_accept_button=False):
    # Создаем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер кнопки с временем
    kb_builder.row(*[InlineKeyboardButton(
        text=time,
        callback_data=time) for time in list_with_time], width=3)
    # Добавляем кнопкy подтвердить в билдер
    if is_accept_button:
        accept_button: InlineKeyboardButton = InlineKeyboardButton(
            text='✅️ Подвердить',
            callback_data='accept_button_press')
        kb_builder.row(*[accept_button])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()