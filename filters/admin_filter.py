from config_data.config import load_config, Config
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import load_config

config: Config = load_config()

class IsAdmin(BaseFilter):
    def __init__(self):
        self.ADMIN_IDS = config.tg_bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in self.ADMIN_IDS:
            return True
        return False