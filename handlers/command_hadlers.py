from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from database.database import user_dict_template, users_db
from filters import PRE_START, CHECK_NUMBER
from keyboards import *
from lexicon.lexicon import LEXICON
from servises.file_handling import my_book


Command_router = Router()
# Нет декоратора роутера !
async def skip_repeat_text_window(message:Message):
    """Эта асинхронная функция удаляет открытую прежде страницу, если юзер нажал
    на какую нибудь кнопку создающее новое окно, а не редактирующее старое с текстом"""
    current_text = my_book[users_db[message.from_user.id]['page']]
    #  В словарь пользователя я добавил ещё одну пару
    #  users_db[message.from_user.id]['reading process'] = []
    if not users_db[message.from_user.id]['reading process']:  # если в списке ещё нет ЭК Message
        att = await message.answer(   # создаю переменную, которая ссылается на ответ бота
            text=current_text,
            reply_markup=create_pagination_keyboard(users_db[message.from_user.id]['page']))
        users_db[message.from_user.id]['reading process'].append(att)  # добаляю ее в словарь юзера
    else:  #  Если в списке уже что-то есть, нам нужно ориенироваться на последний элемент
        last_message = users_db[message.from_user.id]['reading process'].pop()  # получаю его
        await last_message.delete()  #  этим эвэйтом удаляю сообщение на который ссылается last_message
        att = await message.answer(   #  И создаю новую ссылкус ожновременным эвэйтом
            text=current_text,
            reply_markup=create_pagination_keyboard(users_db[message.from_user.id]['page']))
        users_db[message.from_user.id]['reading process'].append(att)

@Command_router.message(CommandStart())
async def process_start_command(message: Message):
    print("Start")
    await message.answer(text=LEXICON[message.text],
                         reply_markup = ReplyKeyboardRemove())
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

@Command_router.message(PRE_START())
async def before_start(message:Message):
    await message.answer(text='Нажми на кнопку <b>start</b> !',
                         reply_markup=pre_start_clava)

@Command_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@Command_router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    await skip_repeat_text_window(message)



@Command_router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    await skip_repeat_text_window(message)


@Command_router.message(CHECK_NUMBER())
async def set_page_number(message:Message):
    print('set_number works\n\n')
    if message.text.startswith('/'):
        users_db[message.from_user.id]['page'] = int(message.text[1:])
    else:
        users_db[message.from_user.id]['page'] = int(message.text)
    await skip_repeat_text_window(message)



# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@Command_router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])