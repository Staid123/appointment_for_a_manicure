from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import months
from services.file_handling import day_in_months
import time


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


def enter_date_working_keyboard(month):
    # Создаем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем месяц первой кнопкой в билдер
    kb_builder.row(InlineKeyboardButton(
        text=month,
        callback_data=f'{month}_button_press'
    ))
    # Добавляем дни месяца в билдер(5 рядов по 7 кнопок в каждом)
    lst_dates = day_in_months(time.strftime('%Y'), month)
    kb_builder.row(*[InlineKeyboardButton(
        text=date,
        callback_data=date) '-' for date in lst_dates if date == 0 else date], width=7)