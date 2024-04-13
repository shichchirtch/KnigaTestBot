from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database import users_db

class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()


class PRE_START(BaseFilter):
    async def __call__(self, message: Message):
        if message.from_user.id not in users_db:
            return True
        return False
