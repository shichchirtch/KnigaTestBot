from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from database import users_db
from servises import my_book

BOOK_LENGTH = len(my_book)


def create_three_button_kbd(user_id: int):
    """ Возвращает инлайн клавиатуру пагинации """
    page = users_db[user_id]["page"]
    buttons = ['backward', f'{page}/{BOOK_LENGTH}', 'forward']
    # для первой и последней страницы лишние кнопки не показываются
    buttons = buttons[1:] if page == 1 else buttons[:-1] if page == BOOK_LENGTH else buttons
    return create_pagination_keyboard(*buttons)


# Функция, генерирующая клавиатуру для страницы книги
# def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
#     # Инициализируем билдер
#     kb_builder = InlineKeyboardBuilder()
#     # Добавляем в билдер ряд с кнопками
#     kb_builder.row(*[InlineKeyboardButton(
#         text=LEXICON[button] if button in LEXICON else button,
#         callback_data=button) for button in buttons]
#     )
#     # Возвращаем объект инлайн-клавиатуры
#     return kb_builder.as_markup()


def create_pagination_keyboard(page=1) -> InlineKeyboardMarkup:
    forward_button = InlineKeyboardButton(text=f'>>', callback_data='forward')
    middle_button = InlineKeyboardButton(text=f'{page} / {len(my_book)}', callback_data=f'{page} / {len(my_book)}')
    backward_button = InlineKeyboardButton(text='<<', callback_data='backward')
    if page == 1:
        pagination_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[middle_button, forward_button]])
        return pagination_keyboard
    elif 1 < page < len(my_book):
        pagination_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[backward_button, middle_button, forward_button]])
        return pagination_keyboard
    else:
        pagination_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[backward_button, middle_button]])
        return pagination_keyboard
