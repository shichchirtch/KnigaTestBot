from aiogram import F, Router
from filters import *
from keyboards.bookmarks_kb import create_edit_keyboard
from keyboards import create_pagination_keyboard
from lexicon import LEXICON
from servises import *
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db

Lese_router = Router()



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@Lese_router.callback_query(MOVE_PAGE())
async def page_moving(callback: CallbackQuery):
    print(f'{callback.data = }')
    shift = -1 if callback.data == 'backward' else 1
    user_id = callback.from_user.id
    users_db[user_id]['page'] += shift
    current_text = my_book[users_db[callback.from_user.id]['page']]
    await callback.message.edit_text(
        text=current_text,
        reply_markup=create_pagination_keyboard( users_db[user_id]['page']
        )
    )
    await callback.answer()



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@Lese_router.callback_query(lambda x: '/' in x.data and x.data.replace(' / ', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки!')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@Lese_router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    zakladka_text = my_book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=zakladka_text,
        reply_markup=create_pagination_keyboard(users_db[callback.from_user.id]["page"]
        )
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@Lese_router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]["bookmarks"]
        )
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@Lese_router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@Lese_router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await (
                callback.message.edit_text(
                text=LEXICON['/bookmarks'],
                reply_markup=create_edit_keyboard(
                    *users_db[callback.from_user.id]["bookmarks"])))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()