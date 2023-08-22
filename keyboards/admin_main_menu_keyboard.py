from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LEXICON_admin_commands


# Функция для настройки кнопки Menu бота для админа
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command, description in LEXICON_admin_commands.items()]
    await bot.set_my_commands(main_menu_commands)