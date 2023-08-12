from aiogram import Router
from aiogram.filters import CommandStart, Command, Text, StateFilter
from lexicon.lexicon_ru import LEXICON_admin, months
from aiogram.fsm.context import FSMContext
from database.tatyana_working import get_connection, init_db, add_messages
from states.admin_state import FSMadmin
from aiogram.fsm.state import default_state
from filters.admin_filter import IsAdmin
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.admin_keyboards import yes_no_keyboard, enter_month_keyboard, enter_date_working_keyboard

# Регистрируем роутер
router: Router = Router()

# Настраиваем фильтр для роутера, чтобы все команды были доступны только админам
router.message.filter(IsAdmin())


# Этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему приветственное сообщение
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    keyboard = yes_no_keyboard()
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_admin['/start'],
                         reply_markup=keyboard)


# Этот хэндлер будет срабатывать если админ не захочет
# настраивать свой график работы
@router.callback_query(Text(text='no_button_press'), StateFilter(default_state))
async def process_no_button_press(callback: CallbackQuery):
    # Удаляем предыдущее сообщение с кнопками, чтобы у пользователя
    # не было желания на них понажимать
    await callback.message.delete()
    # Отправляем пользователю сообщение
    await callback.message.answer(text=LEXICON_admin['no_button_press'])


# Этот хэндлер будет срабатывать если админ захочет
# настроить свой график работы
@router.callback_query(Text(text='yes_button_press'), StateFilter(default_state))
async def process_yes_button_press(callback: CallbackQuery, state: FSMContext):
    print(callback.from_user.first_name)
    keyboard = enter_month_keyboard()
    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.edit_text(text=LEXICON_admin['yes_button_press'],
                                     reply_markup=keyboard)
    await state.set_state(FSMadmin.fill_enter_month)


# Этот хэндлер будет срабатывать на команду cancel
# когда состояние не равняется обычному
@router.callback_query(Text(text='cancel_button_press'), ~StateFilter(default_state))
async def process_cancel_button_press(callback: CallbackQuery, state: FSMContext):
    # Удаляем предыдущее сообщение с кнопками, чтобы у пользователя
    # не было желания на них понажимать
    await callback.message.delete()
    # Отправляем пользователю сообщение
    await callback.message.answer(text=LEXICON_admin['no_button_press'])
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать по нажатию
# месяца с которого мастер начнет принимать клиентов
@router.callback_query(Text(text=months.keys()), StateFilter(FSMadmin.fill_enter_month))
async def process_month_button_press(callback: CallbackQuery, state: FSMContext):
    # Инициализируем базу данных если отсутствует
    init_db()
    # Принимаем клавиатуру
    keyboard: InlineKeyboardMarkup = enter_date_working_keyboard(months[callback.data])
    # Отправим пользователю сообщение с клавиатурой где находятся все дни месяца
    await callback.message.edit_text(text=LEXICON_admin['month_button_press'],
                                     reply_markup=keyboard)
    await state.set_state(FSMadmin.fill_enter_working_date)