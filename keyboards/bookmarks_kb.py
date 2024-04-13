from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from servises import my_book


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{button} - {my_book[button][:100]}',
            callback_data=str(button)
        ))
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        ),
        width=2
    )
    return kb_builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {button} - {my_book[button][:100]}',
            callback_data=f'{button}del'
        ))
    # Добавляем в конец клавиатуры кнопку "Отменить"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        )
    )
    return kb_builder.as_markup()