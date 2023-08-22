from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from lexicon.lexicon_ru import LEXICON_user, LEXICON_admin, months
from services.file_handling import check_phone_number, format_func3
from database.tatiana_working import get_some_records
from database.client_database import AddRecord, CountRecords, GetRecords



# Регистрируем роутер
router: Router = Router()


# Этот хэндлер будет срабатывать на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    # Отправляем пользователю приветственное сообщение и просим его ввести номер телефона
    await message.answer(text=f'Здравствуйте {message.from_user.first_name}!\n\nВведите ваш номер телефона\n(пример: 0685438150)')


# Этот хэндлер будет срабатывать на ввод номера телефона пользователя
@router.message(F.text.isdigit())
async def enter_phone_number(message: Message):
    # Проверяем правильно ли ввёл админ номер телефона клиента
    check = check_phone_number(message.text)
    # Проверяем записан ли пользователь
    records = get_some_records(message.text)
    # Если есть, то инициализируем базу данных если она отсутствует
    if check and records:
        # Создаем цикл и проходим по записям
        for record in records:
            # Получаем данные пользователя
            client_name: str = record[0]
            type_of_service: str = record[5]
            date: str = f'{str(record[1])}.{str(record[2])}.{str(record[3])}.{record[4]}'
            # Создаем экземпляр класса CountRecords
            ex = CountRecords(client_name, type_of_service, date, message.text, message.from_user.id)
            # Проверяем нету ли пользователя уже в базе данных
            count_records = ex.count_records()
            # Если нету то записываем в базу данныx
            if not count_records:
                # Создаем экземпляр класса
                client =  AddRecord(client_name, type_of_service, date, message.text, message.from_user.id)
                # Записываем их в базу
                client.add_record()
            # Благодарим пользователя и предлагаем ему посмотреть на когда он записан
            # командой /see_my_records
            await message.answer(text=LEXICON_user['phone_number_all_good'])
    elif not check:
        await message.answer(text=LEXICON_admin['bad_phone_number'])
    else:
        await message.answer(text=LEXICON_user['not recorded'])


# Этот хэндлер будет срабатывать на ввод команды see_my_records
@router.message(Command(commands=['see_my_records']))
async def command_see_my_records(message: Message):
    # Получаем экземпляр класса
    ex = GetRecords(user_id=message.from_user.id)
    # Проверяем есть ли пользователь в базе данных
    records = ex.get_records()
    # Если есть
    if records:
        # Получаем отфарматированный текст с инфомрацией для пользователя
        msg = format_func3(records, months)
        # Отправляем пользователю сообщение
        await message.answer(text=msg)
    # Если нету
    else:
        # Отправляем пользователю сообщение с просьбой ввести свой номер телефона
        await message.answer(LEXICON_user['not_registered'])