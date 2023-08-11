from aiogram import Router
from aiogram.filters import CommandStart, Command, Text, StateFilter
from lexicon.lexicon_ru import LEXICON_admin
from aiogram.fsm.context import FSMContext
from database.tatyana_working import get_connection, init_db, add_messages
from states.admin_state import FSMadmin
from aiogram.fsm.state import default_state
from filters.admin_filter import IsAdmin
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Регистрируем роутер
router: Router = Router()

# Настраиваем фильтр для роутера, чтобы все команды были доступны только админам
router.message.filter(IsAdmin())


# Этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему приветственное сообщение
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    # Создаем кнопки Да и Нет
    yes_button: InlineKeyboardButton = InlineKeyboardButton(text='Да',
                                                            callback_data='yes_button_press')
    no_button: InlineKeyboardButton = InlineKeyboardButton(text='Нет',
                                                           callback_data='no_button_press')
    # Создаем объект клавиатуры
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button]]
    # Создаем клавиатуру
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_admin['/start'],
                         reply_markup=markup)


@router.callback_query(Text(text='no_button_press'), StateFilter(default_state))
async def process_no_button_press(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_admin['no_button_press'])