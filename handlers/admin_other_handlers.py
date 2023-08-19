from aiogram import Router
from aiogram.filters import StateFilter, Text
from aiogram.fsm.state import default_state
from aiogram.types import Message
from filters.admin_filter import IsAdmin
from lexicon.lexicon_ru import LEXICON_admin, LEXICON_admin_commands


# Регистрируем роутер
router: Router = Router()

# Настраиваем фильтр для роутера, чтобы все команды были доступны только админам
router.message.filter(IsAdmin())


# Этот хэндлер будет реагировать на любые сообщения админа в обычном состоянии,
# не предусмотренные логикой работы бота
@router.message(StateFilter(default_state), ~Text(text=[LEXICON_admin_commands.keys()]))
async def other_message_default_state(message: Message):
    # Отправляем пользователю сообщение
    await message.answer(text=LEXICON_admin['other_message_default_state'])


# Этот хэндлер будет реагировать на любые сообщения админа не в обычном состоянии,
# не предусмотренные логикой работы бота
@router.message(~StateFilter(default_state))
async def other_message_not_default_state(message: Message):
    # Отправляем пользователю сообщение
    await message.answer(text=LEXICON_admin['other_message_not_default_state'])