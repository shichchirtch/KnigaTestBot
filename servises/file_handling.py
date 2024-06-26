import os
import sys

BOOK_PATH = 'book/БотКнигаЭкзампл.txt'
PAGE_SIZE = 1050

my_book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int = PAGE_SIZE) -> tuple[str, int]:
    extra_letters = 0  # Счётчик количества символов, которые потом нужно отсечь от страницы
    kit = '.,?!;:'
    rest_text = len(text) - start  # Нужно узанать, сколько тектса осталось, чтобы не вызвать ошибку index out of range
    if size - 1 > rest_text:  # Если заданный размер страницы больше чем остаток текста, то
        size = rest_text  # переприсваиваем значение остатка текста -> размеру страницы
    #  Проверяю, чтобы страница была меньше остатка текста и чтобы символ,
    #  следующий за концом страницы был в наборе знаков препинания
    if len(text[start:start + size]) < rest_text and text[start + size] in kit:
        size = size - 2  # если это так - уменьшаю размер странцы на 2,
        # потому что только многоточие имеет длину 3
        # хорошо что не было много смйликов)))))
    main_chunk = text[start: start + size]  # вырезаю кусок текста под страницу

    revers_main_chunk = main_chunk[::-1]
    for letter in revers_main_chunk:  # нас интересует только конец страницы
        if letter not in kit:  # Если символ не в наборе
            extra_letters += 1  # то плюсую счётчик
        else:
            break  # дойдя до первого знака препинания - выхожу из цикла
    new_str = main_chunk[:size - extra_letters]  # делаю срез по формату страницы
    return new_str, len(new_str)


# Функция, формирующая словарь книги
def prepare_book(path: str = BOOK_PATH) -> None:
    with open(path, 'r') as file:
        str_file = file.read()
        start = count = 0
        for letter in range(start, len(str_file), PAGE_SIZE):
            page_text, sinboll_index = _get_part_text(str_file, start, PAGE_SIZE)
            count += 1
            my_book[count] = page_text.lstrip()
            start += sinboll_index


# Вызов функции prepare_book для подготовки книги из текстового файла
# print(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))


