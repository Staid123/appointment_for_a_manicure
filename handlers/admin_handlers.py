from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Text, StateFilter, or_f, Command
from lexicon.lexicon_ru import LEXICON_admin, months, LEXICON_admin_commands, LEXICON_admin_type_of_service
from aiogram.fsm.context import FSMContext
from database.tatiana_working import (init_db, add_year, get_year, add_month, get_month, add_day, delete_last_record,
                                       insert_new_record, how_many_time, get_all_records, add_client_name, add_phone_number,
                                       get_client_name, get_phone_number, delete_some_record, get_service, add_type_of_service)
from states.admin_state import FSMadmin
from aiogram.fsm.state import default_state
from filters.admin_filter import IsAdmin
from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from keyboards.admin_keyboards import (yes_no_keyboard, enter_month_keyboard, enter_date_working_keyboard,
                                        enter_time_working_keyboard, edit_working_date_keyboard, enter_type_of_service_keyboard)
from services.file_handling import check_phone_number, working_time_in_day, format_func1, format_func2



# Регистрируем роутер
router: Router = Router()

# Настраиваем фильтр для роутера, чтобы все команды были доступны только админам
router.message.filter(IsAdmin())


# Этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему приветственное сообщение
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    # await bot.send_message(chat_id=message.from_user.id, text='Hello')
    keyboard = yes_no_keyboard()
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_admin['/start'],
                         reply_markup=keyboard)
    # Устанавливаем состояние ожидания ответа на сообщение
    await state.set_state(FSMadmin.fill_yes_no_in_start)


# Этот хэндлер будет срабатывать если админ не захочет
# настраивать свой график работы
@router.callback_query(Text(text='no_button_press'), StateFilter(FSMadmin.fill_yes_no_in_start))
async def process_no_button_press(callback: CallbackQuery, state: FSMContext):
    # Удаляем предыдущее сообщение с кнопками, чтобы у пользователя
    # не было желания на них понажимать
    await callback.message.delete()
    # Отправляем пользователю сообщение
    await callback.message.answer(text=LEXICON_admin['no_button_press'])
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать если админ захочет 
# настраивать свой график работы
@router.callback_query(Text(text='yes_button_press'), StateFilter(FSMadmin.fill_yes_no_in_start))
async def process_yes_button_press(callback: CallbackQuery, state: FSMContext):
    # Инициализируем базу данных если отсутствует
    init_db()
    # Удаляем клавиатуру чтобы пользователь не нажимал на кнопки
    await callback.message.delete()
    # Благодарим пользователя и просим его ввести имя клиента
    await callback.message.answer(text=LEXICON_admin['yes_button_press'])
    # Отправляем пользователю колбэк чтобы нажатая кнопка не светилась долго
    await callback.answer()
    # Устанавливаем состояние ожидания ввода имени клиента
    await state.set_state(FSMadmin.fill_enter_client_name)


# Этот хэндлер будет срабатывать при вводе имени клиента
@router.message(F.text.isalpha(), StateFilter(FSMadmin.fill_enter_client_name))
async def process_enter_client_name(message: Message, state: FSMContext):
    # Записываем имя клиента в базу данных
    add_client_name(message.text.capitalize())
    # Отправляем сообщение с просьбой ввести номер телефона клиента
    await message.answer(text=LEXICON_admin['client_phone_number'])
    # Устанавливаем состояние ожидания ввода номера телефона клиента
    await state.set_state(FSMadmin.fill_enter_client_phone_number)


# Этот хэндлер будет срабатывать на ввод номера телефона клиента
@router.message(StateFilter(FSMadmin.fill_enter_client_phone_number))
async def process_enter_client_phone_number(message: Message, state: FSMContext):
    # Проверяем правильно ли ввёл админ номер телефона клиента
    check = check_phone_number(message.text)
    # Если номер телефона введен неправильно, то сообщаем это пользователю и просим ввести номер телефона заново
    if not check:
        await message.answer(LEXICON_admin['bad_phone_number'])
    else:
        # Записываем номер телефона в базу данных
        add_phone_number(f'{str(message.text)}')
        # Отправляем сообщение пользователю с просьбой ввести год
        await message.answer(LEXICON_admin['good_phone_number'])
        # Устанавливаем состояние ожидания ввода года
        await state.set_state(FSMadmin.fill_enter_year)


# Этот хэндлер будет срабатывать когда админ введет
# год с которого он планирует принимать записи
@router.message(StateFilter(FSMadmin.fill_enter_year), F.text.isdigit())
async def process_year_writing(message: Message, state: FSMContext):
    # Записуем год в базу данных
    add_year(message.text)
    # Принимаем объект инлайн-клавиатуры
    keyboard = enter_month_keyboard()
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_admin['year_wrote'],
                                     reply_markup=keyboard)
    await state.set_state(FSMadmin.fill_enter_month)


# Этот хэндлер будет срабатывать в случае нажатия
# кнопки отмена при указания месяца
@router.callback_query(StateFilter(FSMadmin.fill_enter_month), Text(text='cancel_button_press'))
async def cancel_button_press_month_state(callback: CallbackQuery, state: FSMContext):
    # Удаляем клавиатуру
    await callback.message.delete_reply_markup()
    # Отправляем пользователю сообщение
    await callback.message.edit_text(text=LEXICON_admin['no_button_press'])
    # Удаляем последнюю запись
    delete_last_record()
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
    # Получаем имя клиента, его номер телефона, нынешний год и месяц
    client_name, phone_number, now_year, now_month = get_client_name(), get_phone_number(), get_year(), get_month()
    # Удаляем последнюю запись
    delete_last_record()
    # Проверяем не является ли месяц последним в году и принимаем клавиатуру
    if now_month == 12:
        now_year += 1
        now_month = 1
    else:
        now_month += 1
    keyboard: InlineKeyboardMarkup = enter_date_working_keyboard(now_year, now_month)
    # Записываем в базу данных имя клиента, его номер телефона, новый месяц и год
    add_client_name(client_name)
    add_phone_number(phone_number)
    add_year(now_year)
    add_month(now_month)
    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.edit_text(text=LEXICON_admin['month_button_press'],
                                     reply_markup=keyboard)
    

# Этот хэндлер будет срабатывать на нажатие кнопки назад
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_date), Text(text='backward'))
async def process_backward_button_press(callback: CallbackQuery):
    # Получаем имя клиента, его номер телефона, нынешний год и месяц
    client_name, phone_number, now_year, now_month = get_client_name(), get_phone_number(), get_year(), get_month()
    # Удаляем последнюю запись
    delete_last_record()
    # Проверяем не является ли месяц первым в году и принимаем клавиатуру
    if now_month == 1:
        now_year -= 1
        now_month = 12
    else:
        now_month -= 1
    keyboard: InlineKeyboardMarkup = enter_date_working_keyboard(now_year, now_month)
    # Записываем в базу данных имя клиента, его номер телефона, новый месяц и год
    add_client_name(client_name)
    add_phone_number(phone_number)
    add_year(now_year)
    add_month(now_month)
    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.edit_text(text=LEXICON_admin['month_button_press'],
                                     reply_markup=keyboard)
    

# Этот хэндлер будет срабатывать на нажатие кнопки время
@router.callback_query(StateFilter(FSMadmin.fill_enter_working_time))
async def process_time_button_press(callback: CallbackQuery, state: FSMContext):
    # Записываем в базу данных время записи
    insert_new_record(callback.data)
    # Получаем клавиатуру с видами услуг
    keyboard: InlineKeyboardMarkup = enter_type_of_service_keyboard(LEXICON_admin_type_of_service)
    # Благодарим пользователя и просим ввести вид услуги
    await callback.message.edit_text(
        text=LEXICON_admin['accept_button_press'],
        reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода типа услуг
    await state.set_state(FSMadmin.fill_enter_type_of_service)
    

# Этот хэндлер будет срабатывать при выборе услуги
@router.callback_query(StateFilter(FSMadmin.fill_enter_type_of_service), Text(text=LEXICON_admin_type_of_service))
async def process_enter_type_of_service(callback: CallbackQuery, state: FSMContext):
    # Записываем вид услуги в базу данных
    add_type_of_service(callback.data)
    # Копируем виды услуг
    lst_with_services = deepcopy(LEXICON_admin_type_of_service)
    # Убираем уже нажатые виды услуг
    services = get_service().split(',')
    for service in services:
        del_index = lst_with_services.index(service)
        del lst_with_services[del_index]
    # Получаем клавиатуру с видами услуг уже без нажатых услуг
    keyboard: InlineKeyboardMarkup = enter_type_of_service_keyboard(lst_with_services, is_accept_button=True)
    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.edit_text(
        text=LEXICON_admin['type_of_service_press'],
        reply_markup=keyboard)


# Этот хэндлер будет срабатывать при нажатии кнопки Подтвердить при выборе услуги
@router.callback_query(StateFilter(FSMadmin.fill_enter_type_of_service), Text(text='accept_button_press'))
async def process_accept_button_press(callback: CallbackQuery, state: FSMContext):
    # Убираем клавиатуру
    await callback.message.delete_reply_markup()
    # Предлагаем пользователю посмотреть все доступные ему команды
    await callback.message.edit_text(text=LEXICON_admin['end'])
    # Убираем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на нажатие команды /help
@router.message(StateFilter(default_state), Command(commands=['help']))
async def process_help_command(message: Message):
    # Отправляем словарь с командамми в функцию для форматирования
    res = format_func1(LEXICON_admin_commands)
    # Отправляем пользователю сообщение со списком всех команд
    await message.answer(text=res)


# Этот хэндлер будет срабатывать если админ захочет 
# настраивать свой график работы
@router.message(Command(commands=['add_new_working_date']), StateFilter(default_state))
async def process_add_new_working_date(message: Message, state: FSMContext):
    # Отправляем пользователю сообщение с просьбой его ввести имя клиента
    await message.answer(text=LEXICON_admin['yes_button_press'])
    # Устанавливаем состояние ожидания ввода года
    await state.set_state(FSMadmin.fill_enter_client_name)


# Этот хэндлер будет срабатывать если админ захочет
# посмотреть дни когда он будет работать
@router.message(Command(commands=['check_my_working_dates']), StateFilter(default_state))
async def process_check_my_working_dates(message: Message):
    # Получаем все записи с базы данных
    all_records = get_all_records()
    # Проверяем есть ли записи в базе
    if all_records:
        # Отправляем полученный список кортежей в функцию для форматирования
        res = format_func2(all_records, months)
        # Отправляем пользователю сообщение с его графиком работы
        await message.answer(text=f'{res}\n{LEXICON_admin["check_my_working_dates"]}')
    else:
        # Так как записей нет, то просим пользователя сделать график работы
        await message.answer(text=LEXICON_admin['no_records_in_database'])


# Этот хэндлер будет срабатывать если админ захочет
# изменить свой график работы
@router.message(Command(commands=['edit_my_working_dates']), StateFilter(default_state))
async def process_edit_my_working_dates(message: Message, state: FSMContext):
    # Получаем все записи с базы данных
    all_records = get_all_records()
    # Если нету записей просим пользователя создать свой график работы
    if all_records:
        # Получаем клавиатуру
        keyboard: InlineKeyboardMarkup = edit_working_date_keyboard(all_records, months)
        # Отправляем пользователю сообщение с просьбой изменить свой график работы
        await message.answer(text=LEXICON_admin['edit_working_date'],
                             reply_markup=keyboard)
        # Устанавливаем состояние ожидания изменения графика работы
        await state.set_state(FSMadmin.fill_edit_working_time)
    else:
        await message.answer(text=LEXICON_admin['no_records_in_database'])


# Этот хэндлер будет срабатывать если админ 
# нажмет кнопку отменить при отмене записей
@router.callback_query(StateFilter(FSMadmin.fill_edit_working_time), Text(text='cancel_button_press'))
async def cancel_button_press(callback: CallbackQuery, state: FSMContext):
    # Удаляем клавиатуру
    await callback.message.delete_reply_markup()
    # Предлагаем пользователю посмотреть список доступных ему команд
    await callback.message.edit_text(text=LEXICON_admin['end'])
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать если админ удалит какую-то запись
@router.callback_query(StateFilter(FSMadmin.fill_edit_working_time), Text(startswith='del'))
async def process_delete_record(callback: CallbackQuery, state: FSMContext):
    # Парсим данные
    record = callback.data[3:].split()
    year, month, day, time = int(record[3]), int(record[2]), int(record[1]), record[0]
    # Удаляем запись
    delete_some_record(year, month, day, time)
    # Получаем все записи
    all_records = get_all_records()
    # Если нету записей просим пользователя создать свой график работы
    if all_records:
        # Получаем клавиатуру
        keyboard: InlineKeyboardMarkup = edit_working_date_keyboard(all_records, months, is_accept_button=True)
        # Отправляем пользователю сообщение с просьбой изменить свой график работы
        await callback.message.edit_text(text=callback.message.text,
                             reply_markup=keyboard)
    else:
        # Отправляем пользователю сообщение что записей больше нет и предлагаем посмотреть список доступных ему команд
        await callback.message.edit_text(text=LEXICON_admin['no_records_in_database_after_deleting'])
        # Сбрасываем состояние
        await state.clear()


# Этот хэндлер будет срабатывать когда пользователь нажмет подтвердить
# при отмене записей
@router.callback_query(StateFilter(FSMadmin.fill_edit_working_time), Text(text='accept_button_press'))
async def accept_button_press(callback: CallbackQuery, state: FSMContext):
    # Удаляем клавиатуру
    await callback.message.delete_reply_markup()
    # Благодарим пользователя и отправляем ему список всех команд
    await callback.message.edit_text(text=LEXICON_admin['end'])
    # Сбрасываем состояние
    await state.clear()