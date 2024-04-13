from aiogram import Router
from aiogram.types import Message

Other_router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@Other_router.message()
async def send_echo(message: Message):
    await message.reply(f'Это эхо! {message.text}')