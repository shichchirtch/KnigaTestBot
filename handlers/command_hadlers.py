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


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
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

# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@Command_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@Command_router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    current_text = my_book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=current_text,
        reply_markup=create_pagination_keyboard( users_db[message.from_user.id]['page']
        )
    )


# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@Command_router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    current_text = my_book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=current_text,
        reply_markup=create_pagination_keyboard(
            users_db[message.from_user.id]["page"]
        )
    )

@Command_router.message(CHECK_NUMBER())
async def set_page_number(message:Message):
    print('set_number works\n\n')
    if message.text.startswith('/'):
        users_db[message.from_user.id]['page'] = int(message.text[1:])
    else:
        users_db[message.from_user.id]['page'] = int(message.text)
    current_text = my_book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=current_text,
        reply_markup=create_pagination_keyboard(
            users_db[message.from_user.id]["page"]
        )
    )



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