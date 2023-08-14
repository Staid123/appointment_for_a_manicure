from aiogram import Router, F
from aiogram.filters import CommandStart, Text, StateFilter, or_f
from lexicon.lexicon_ru import LEXICON_admin, months, LEXICON_admin_commands
from aiogram.fsm.context import FSMContext
from database.tatiana_working import init_db, add_year, get_year, add_month, get_month, add_day, delete_record, insert_new_record, how_many_time
from states.admin_state import FSMadmin
from aiogram.fsm.state import default_state
from filters.admin_filter import IsAdmin
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from keyboards.admin_keyboards import yes_no_keyboard, enter_month_keyboard, enter_date_working_keyboard, enter_time_working_keyboard
from services.file_handling import working_time_in_day

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
# настраивать свой график работы
@router.callback_query(Text(text='yes_button_press'), StateFilter(default_state))
async def process_yes_button_press(callback: CallbackQuery, state: FSMContext):
    # Удаляем клавиатуру чтобы пользователь не нажимал на кнопки
    await callback.message.delete()
    # Благодарим пользователя и просим его ввести год
    await callback.message.answer(text=LEXICON_admin['yes_button_press'])
    # Отправляем пользователю колбэк чтобы нажатая кнопка не светилась долго
    await callback.answer()
    # Устанавливаем состояние ожидания ввода года
    await state.set_state(FSMadmin.fill_enter_year)


# Этот хэндлер будет срабатывать когда админ введет
# год с которого он планирует принимать записи
@router.message(StateFilter(FSMadmin.fill_enter_year), F.text.isdigit())
async def process_yes_button_press(message: Message, state: FSMContext):
    # Инициализируем базу данных если отсутствует
    init_db(force=True)
    # Записуем год в базу данных
    add_year(message.text)
    # Принимаем объект инлайн-клавиатуры
    keyboard = enter_month_keyboard()
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_admin['year_wrote'],
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
    # Получаем нынешний год
    now_year = get_year()
    # Отправляем в базу месяц
    add_month(callback.data)
    # Принимаем клавиатуру
    keyboard: InlineKeyboardMarkup = enter_date_working_keyboard(now_year, callback.data)
    # Отправим пользователю сообщение с клавиатурой где находятся все дни месяца
    await callback.message.edit_text(text=LEXICON_admin['month_button_press'],
                                     reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода даты
    await state.set_state(FSMadmin.fill_enter_working_date)


# Этот хэндлер будет срабатывать на нажатие кнопки месяца
# при выборе дат приема записей
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_date), or_f(Text(endswith='_button_press'), Text(startswith='-')))
async def bad_process_month_button_press(callback: CallbackQuery):
    # Отправляем пользователю сообщение с просьбой выбрать дату приема записей
    await callback.answer(text=LEXICON_admin['bad_month_button_press'],
                          show_alert=True)
    

# Этот хэндлер будет срабатывать на нажатие даты
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_date), Text(endswith='date'))
async def process_date_button_press(callback: CallbackQuery, state: FSMContext):
    # Отправляем в базу дату
    add_day(callback.data[:-4])
    # Принимаем список с временем когда пользователь будет работать
    list_with_time = working_time_in_day()
    # Отправляем пользователю сообщение с клавиатурой с просьбой выбрать время записи
    keyboard: InlineKeyboardMarkup = enter_time_working_keyboard(list_with_time)
    # Отправим пользователю сообщение с клавиатурой со временем работы
    await callback.message.edit_text(text=LEXICON_admin['good_month_button_press'],
                                     reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода времени
    await state.set_state(FSMadmin.fill_enter_working_time)


# Этот хэндлер будет срабатывать на нажатие кнопки вперед
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_date), Text(text='forward'))
async def process_forward_button_press(callback: CallbackQuery):
    # Получаем нынешний год из базы данных
    now_year = get_year()
    # Получаем нынешний месяц из базы данных
    now_month = get_month()
    # Удаляем записи с этим месяцем и годом
    delete_record()
    # Проверяем не является ли месяц последним в году и принимаем клавиатуру
    if now_month == 12:
        now_year += 1
        now_month = 1
    else:
        now_month += 1
    keyboard: InlineKeyboardMarkup = enter_date_working_keyboard(now_year, now_month)
    # Записываем в базу данных новый месяц и год
    add_year(now_year)
    add_month(now_month)
    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.edit_text(text=LEXICON_admin['month_button_press'],
                                     reply_markup=keyboard)
    

# Этот хэндлер будет срабатывать на нажатие кнопки назад
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_date), Text(text='backward'))
async def process_backward_button_press(callback: CallbackQuery):
    # Получаем нынешний год из базы данных
    now_year = get_year()
    # Получаем нынешний месяц из базы данных
    now_month = get_month()
    # Удаляем записи с этим месяцем и годом
    delete_record()
    # Проверяем не является ли месяц первым в году и принимаем клавиатуру
    if now_month == 1:
        now_year -= 1
        now_month = 12
    else:
        now_month -= 1
    keyboard: InlineKeyboardMarkup = enter_date_working_keyboard(now_year, now_month)
    # Записываем в базу данных новый месяц и год
    add_year(now_year)
    add_month(now_month)
    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.edit_text(text=LEXICON_admin['month_button_press'],
                                     reply_markup=keyboard)
    

# Этот хэндлер будет срабатывать на нажатие кнопки время
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_time), Text(endswith=':00'))
async def process_time_button_press(callback: CallbackQuery):
    # Записываем в базу данных время записи
    insert_new_record(callback.data)
    # Принимаем список с временем когда пользователь будет работать
    list_with_times = working_time_in_day()
    # Получаем список с вренем когда пользователь же работает
    list_with_how_many_time = how_many_time()
    # Убираем с этого списка выбраное пользователем время
    for time in list_with_how_many_time:
        del_index = list_with_times.index(time[0])
        del list_with_times[del_index]
    # Получаем клавиатуру
    if not list_with_how_many_time:
        keyboard: InlineKeyboardMarkup = enter_time_working_keyboard(list_with_times)
    else:
        keyboard: InlineKeyboardMarkup = enter_time_working_keyboard(list_with_times, is_accept_button=True)
    # Отправляем пользователю сообщение с предложением продолжить выбор времени в которое он будет работать
    await callback.message.edit_text(text=LEXICON_admin['time_button_press'], 
                                     reply_markup=keyboard)
    

# Этот хэндлер будет срабатывать на нажатие кнопки подтвердить при выборе времениэ
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_time), Text(text='accept_button_press'))
async def process_accept_button_press(callback: CallbackQuery, state: FSMContext):
    # Удаляем клавиатуру
    callback.message.delete_reply_markup()
    # Благодарим пользователя и выводим доступные ему команды для использования
    await callback.message.edit_text(text=LEXICON_admin['accept_button_press'])
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие команды /help
@router.message(StateFilter(default_state), Text(text='/help'))
async def process_help_command(message: Message, state: FSMContext):
    res: str = str()
    for command, text in LEXICON_admin_commands.items():
        res += (f'{command}\n{text}\n\n')
    # Отправляем пользователю сообщение со списком всех команд
    await message.answer(text=res)