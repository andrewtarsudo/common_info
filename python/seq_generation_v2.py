from typing import Optional
import numpy


def get_doc_ranges(doc_num: int, doc_pages: int) -> tuple[int, int]:
    """
    Get the doc start and end pages.

    :param int doc_num: the document ordinal number
    :param int doc_pages: the page number in the document
    :return: the first and the last page.
    :rtype: tuple[int, int]
    """
    return 1 + doc_num * doc_pages, (1 + doc_num) * doc_pages


def _get_str_doc_ranges(start_page: int, end_page: int) -> str:
    """
    Join the start and end pages to the one string.

    :param int start_page: the start page
    :param int end_page: the end page
    :return: the unified string.
    :rtype: str
    """
    return "-".join((str(start_page), str(end_page)))


def _correct_input(user_input: str) -> Optional[int]:
    """
    Validate the user input.

    :param str user_input: the user input
    :return: the integer
    :rtype: int or None
    """
    try:
        res = int(user_input)
    except ValueError:
        print("Введено не целое число.")
        return None
    except OSError as e:
        print(f"Ошибка ввода. {e.errno}, {e.strerror}")
        return None
    else:
        if res < 0:
            print("Введенное число отрицательное. Будет использован модуль числа.")
            return numpy.abs(res)
        else:
            return res


def main():
    # validate the number of pages in the docs
    while True:
        num_pages_user_input = input("Введите количество страниц одного документа:\n")
        num_pages = _correct_input(num_pages_user_input)
        if num_pages is None:
            continue
        else:
            break
    # validate the number of docs
    while True:
        doc_num_user_input = input("Введите количество документов:\n")
        doc_num = _correct_input(doc_num_user_input)
        if doc_num is None:
            continue
        else:
            break

    list_strings = []
    start_doc_num = 0
    # get the list of strings for docs
    while start_doc_num < doc_num:
        start_page, end_page = get_doc_ranges(start_doc_num, num_pages)
        list_strings.append(_get_str_doc_ranges(start_page, end_page))
        start_doc_num += 1

    print(",".join(list_strings))

    input("Нажмите любую клавишу, чтобы закрыть программу...\n")


if __name__ == "__main__":
    main()
