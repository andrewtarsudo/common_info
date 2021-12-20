import re
import fitz
import easyocr
import pathlib
import os
from operator import sub

rect_A3 = fitz.IRect(832, 664, 1160, 700)
rect_A4 = fitz.IRect(238, 706, 568, 747)

INDECES = {5, 6, 7, 8, 9, 10, 12, 13, 14}

pattern = r'ПАМР\.\d{6}\.\d{3}-?\d*[а-яА-Я]*-?[а-яА-Я]*'


def rect_proper(rect: fitz.Rect) -> fitz.Rect:
    if not rect.is_valid:
        rect.normalize()
    return rect


def page_orientation(rect: fitz.Rect) -> str:
    if rect.height > rect.width:
        return 'portrait'
    elif rect.height < rect.width:
        return 'landscape'
    else:
        return 'INCORRECT_ORIENT'


def eps_neighbour(rect: fitz.Rect, page_format: str, eps: int = 1) -> bool:
    rect_size = rect.width, rect.height
    return any(val > eps for val in sub(fitz.paper_size(page_format), rect_size))


def page_info(rect: fitz.Rect) -> tuple:
    orient = page_orientation(rect)
    if orient == 'INCORRECT_ORIENT':
        return 'NON-STANDARD', orient

    if orient == 'portrait':
        if not eps_neighbour(rect, 'A4-p'):
            return 'A4', orient
        elif not eps_neighbour(rect, 'A3-p'):
            return 'A3', orient
        else:
            return 'NON-STANDARD', orient

    if orient == 'landscape':
        if not eps_neighbour(rect, 'A4-l'):
            return 'A4', orient
        elif not eps_neighbour(rect, 'A3-l'):
            return 'A3', orient
        else:
            return 'NON-STANDARD', orient


def rect_extract(format_page: str, orient: str) -> fitz.Rect:
    if format_page == 'NON-STANDARD':
        return fitz.EMPTY_RECT()

    if (format_page, orient) == ('A4', 'portrait'):
        return rect_A4
    elif (format_page, orient) == ('A3', 'landscape'):
        return rect_A3
    else:
        return fitz.EMPTY_RECT()


def create_png(page_doc: fitz.Page, rect: fitz.Rect, path):
    if not rect.is_empty():
        pix = page_doc.get_pixmap(clip=rect.irect)
    else:
        pix = page_doc.get_pixmap()

    pix.save(path, output='png')
    return path


def text_pattern(text: str):
    return bool(re.match(pattern, text.strip()))


def text_correction(text: str) -> str:
    if len(text) < 15:
        print('Bad name')
        return text

    list_text = list(text)

    if not list_text[4] == '.':
        list_text.insert(4, '.')

    if not list_text[11] == '.':
        list_text.insert(11, '.')

    for index in INDECES:
        if list_text[index] == 'З':
            list_text[index] = '3'

        if list_text[index] == 'О':
            list_text[index] = '0'

    if len(text) > 16 and list_text[-1:-3] == 'СЬБ':
        del list_text[-2]

    if len(text) > 16 and list_text[-1:-2] == 'СЬ':
        list_text[-1] = 'Б'

    return str(list_text)


def main():
    fitz_name_list = []
    easyocr_name_list = []
    reader = easyocr.Reader(['ru'])
    path_file_pdf = ''
    path_file = pathlib.Path(path_file_pdf).resolve()
    page = fitz.Document(path_file_pdf).page_load(0)
    page_rect = page.rect()
    rectangle_extract = rect_extract(page_info(page_rect)[0], page_info(page_rect)[1])
    png_name = path_file.stem + '.png'
    path_file_png = pathlib.PurePath(path_file).with_name(png_name)
    text_fitz = page_rect.get_textbox(rectangle_extract)
    fitz_name_list.append(text_fitz)
    text_easyocr = reader.readtext(create_png(page, rectangle_extract, path_file_png), detail=0, paragraph=True)
    easyocr_name_list.append(text_easyocr)


if __name__ == '__main__':
    main()
