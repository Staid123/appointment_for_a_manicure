from config_data.config import load_config
from aiogram.filters import BaseFilter
from aiogram.types import Message


ADMIN_IDS = 664760823, 2037720596, 5202602677


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in ADMIN_IDS:
            return True
        return False