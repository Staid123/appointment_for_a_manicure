import logging
import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import admin_handlers, admin_other_handlers, user_handlers
from keyboards.admin_main_menu_keyboard import set_main_menu

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
    # Конфигурирем логгирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    # Загружаем конфиг в переменную config
    config: Config = load_config()
    # Регистрируем бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    
    # Настраиваем главное меню бота только для админа
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(admin_handlers.router)
    dp.include_router(admin_other_handlers.router)
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
 
 
if __name__ == '__main__':
    asyncio.run(main())
 