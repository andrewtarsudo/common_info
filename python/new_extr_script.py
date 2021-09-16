import os
import fitz

# const coordinates for the A4 file
UP_LEFT_X_A4 = 320
UP_LEFT_Y_A4 = 950
DOWN_RIGHT_X_A4 = 775
DOWN_RIGHT_Y_A4 = 1110

# const coordinates for the A3 file
UP_LEFT_X_A3 = 1110
UP_LEFT_Y_A3 = 880
DOWN_RIGHT_X_A3 = 1545
DOWN_RIGHT_Y_A3 = 935

words_to_find = ['ПАМР', 'ПДРА']

# determine the rectangle
def rectangle_extr(formatFile):
    if formatFile == 'A4':
        upleft_x = UP_LEFT_X_A4
        upleft_y = UP_LEFT_Y_A4
        downright_x = DOWN_RIGHT_X_A4
        downright_y = DOWN_RIGHT_Y_A4

    elif formatFile == 'A3':
        upleft_x = UP_LEFT_X_A3
        upleft_y = UP_LEFT_Y_A3
        downright_x = DOWN_RIGHT_X_A3
        downright_y = DOWN_RIGHT_Y_A3

    else:
        upleft_x = 0
        upleft_y = 0
        downright_x = manual_input('int', 'x coordinate  of the bottom right point')
        downright_y = manual_input('int', 'y coordinate  of the bottom right point')

    rectangle = fitz.Rect(upleft_x, upleft_y, downright_x, downright_y)

    ans = rectangle
    return ans


def file_format(page):
    lRect_page = page.round()

    if lRect_page.is_empty:
        print('You have some problems. I\'m sorry.')

    if lRect_page.is_infinite:
        lRect_page.normalize()

    if lRect_page.height < 1130 and lRect_page.height > 1120:
        if lRect_page.width < 800 and lRect_page.width > 790:
            format = 'A4'
        elif lRect_page.width < 1580 and lRect_page.width > 1590:
            format = 'A3'
        else:
            format = 'UNKNOWN_FORMAT'
            raise Warning('The format is non-standard.')
    else:
        format = 'PAGE_SIZE_NOT_STANDARD'
        raise Warning('Page dimensions are unspecified')

    ans = format
    return ans


def manual_input(type_input, param):
    type_to_convert = type_input[1:len(type_input)-2]
    def_type = 'int'
    input_user = str(input('Type the value of the parameter %s: '%param))

    try:
        conv_input_user = format(input_user, type_to_convert)
        ans = conv_input_user
    except TypeError:
        print('Incorrect type. The default type (%s) is used instead.'%def_type)
        type_to_convert = def_type[1:len(type_input)-2]
        conv_input_user = format(input_user, type_to_convert)
        ans = conv_input_user

    return ans


def read_pdf(dir_path, filename):
    dir_path = str(input('Type the path to the directory with pdf files: '))
    file_path = pathlib.Path(dir_path).resolve() / filename
    doc = fitz.open(file_path)  # type fitz.Document
    doc_page = doc.load_page(0)  # type fitz.Page

    ans = doc_page
    return ans


def check_text(text):
    if len(text) == 0:
        raise Warning('The text is not extracted.')
        ans = 'not ok'
        return ans

    counter = 1
    for word in words_to_find:
        if text.startswith(word):
            counter = 0
            break

    if counter == 0:
        ans = 'ok'
    elif counter == 1:
        ans = 'not ok'
    else:
        raise Warning('The extracted text format differs the expectation')
        ans = 'not ok'

    return ans


def dir_content_pdf(path_to_dir):
    full_content = os.listdir(path_to_dir)

    for file in full_content:
        if not pathlib.PurePath(file).suffix == '.pdf':
            full_content.remove(file)

    ans = full_content
    return ans


def main():
    full_path_dir = str(input('Type the full path to the file: '))
    path_dir = pathlib.PurePath(full_path_dir).resolve()
    list_new_names = []

    for scan in dir_content_pdf(path_dir):
        file_name = os.path.split(scan).[1]
        page_pdf = read_pdf(path_dir, file_name)
        format = file_format(page_pdf)
        rect = rectangle_extr(format)
        extr_text = page_pdf.get_textbox(rect)
        new_name_full = extr_text + '.pdf'

        if check_text(extr_text) == 'ok':
            os.rename(pathlib.path_dir.joinpath(file_name), pathlib.path_dir.joinpath(new_name_full))
            list_new_names.append(str(pathlib.path_dir.exists()))
        else:
            raise Warning('The text is incorrect.')
            list_new_names.append('False')

    ans = list_new_names
    return ans


main()
