from aiogram import Router
from aiogram.types import Message
from servises import my_book

Other_router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@Other_router.message()
async def send_echo(message: Message):
    if message.text.isdigit():
        await message.reply(f'В книге только  <b>{len(my_book)}</b>  страниц')
    if message.text.isalpha():
        await message.reply(f'Давайте лучше продолжим чтение ?')
