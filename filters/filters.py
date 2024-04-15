from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database import users_db
from servises import my_book


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


class MOVE_PAGE(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        if callback.data in ['forward', 'backward']:
            return True
        return False


class CHECK_NUMBER(BaseFilter):
    async def __call__(self, message: Message):
        if ((message.text.startswith('/') and message.text[1:].isdigit()
             and int(message.text[1:]) < len(my_book)) or
                (message.text.isdigit() and int(message.text) <= len(my_book))):
            return True
        return False
