import os
import pathlib
import fitz
import numpy
import check
import text_correction

# a4 595.2 x 841.69
# a3 1190.4 x 841.69
# const coordinates for the A4 file
UP_LEFT_X_A4 = 250
UP_LEFT_Y_A4 = 650
DOWN_RIGHT_X_A4 = 580
DOWN_RIGHT_Y_A4 = 750
# const coordinates for the A3 file
UP_LEFT_X_A3 = 830
UP_LEFT_Y_A3 = 650
DOWN_RIGHT_X_A3 = 1200
DOWN_RIGHT_Y_A3 = 750
# a list of the symbol combinations to search for
words_to_find = ['ПАМР', 'ПДРА', 'АМР']
# list of improper renamed files
list_bad_names = []

TYPE_FILE_SUFFIX = '.pdf'


# path_pdf_file - full path to the file of Path() type
# output - the parameters of list() with width of int type and height of int() type
# get the page and its dimensions to analyze


def get_page(path_pdf_file: pathlib.PurePath) -> fitz.Page:
    doc = fitz.open(path_pdf_file)
    return doc.load_page(0)


def get_page_bound_pdf(path_pdf_file: pathlib.PurePath) -> tuple:
    page_file_pdf = get_page(path_pdf_file)
    # round the height and the width since it can be float but it's not good to compare numerics of different types
    Rect = page_file_pdf.rect

    return Rect.irect.top_left, Rect.irect.bottom_right, Rect.irect.width, Rect.irect.height


# rect_width and rect_height - the width and the height of the page of int() type
# output - the page format of str() type
# define the format
def get_format(rect_width: int, rect_height: int) -> str:
    # define the most common formats
    page_sizes = (rect_width, rect_height)

    for index in range(0, 1):
        if numpy.abs(page_sizes[index] - fitz.paper_size('A4')[index]) <= 2:
            orientation = 'landscape'
            return 'A4'  # 595.2 x 841.69

        elif numpy.abs(page_sizes[index] - fitz.paper_size('A3')[1 - index]) <= 2:
            orientation = 'portrait'
            return 'A3'  # 1190.4 x 841.69

        else:
            # show the warning but continue operating
            print('Page dimensions are unspecified.')
            return 'PAGE_SIZE_NOT_STANDARD'


# formatFile - the typographic format A#: ..., A3, A4, A5, ... of str() type
# output - rectangle of fitz.Rect() type
# define the rectangle
def get_rectangle_extr(format_file: str) -> tuple:
    # format A4, the common sheet
    if format_file == 'A4':
        return UP_LEFT_X_A4, UP_LEFT_Y_A4, DOWN_RIGHT_X_A4, DOWN_RIGHT_Y_A4
    # format A3, two common sheets
    elif format_file == 'A3':
        return UP_LEFT_X_A3, UP_LEFT_Y_A3, DOWN_RIGHT_X_A3, DOWN_RIGHT_Y_A3
    # another format, input its width and height
    else:
        return 0, 0, DOWN_RIGHT_X_A3, DOWN_RIGHT_Y_A3


# path_to_dir - the full path to the directory with pdf files of str() or Path() type
# output - the list of the files with *.pdf extension inside the directory of list() type with items of Path() type
# get the specific contents of the directory
def dir_content_specified(path_to_dir: pathlib.Path) -> list:
    full_content = os.listdir(path_to_dir)
    # transform needed strings to paths of Path() type
    return [file for file in full_content if pathlib.PurePath(file).suffix == TYPE_FILE_SUFFIX]


# path_file_full - path to the file of path() type
# output - void
# the main activity for one file
def main_one_file(path_file_full: pathlib.PurePath) -> pathlib.PurePath:
    # Algo:
    # measure its dimensions -> get_page_bound_pdf
    # find its format -> get_format
    # define the rectangle for the textbox to extract the text -> get_rectangle_extr
    # create the rectangle -> fitz.Rect
    # extract the text -> fitz.Page.get_textbox
    # clear all links to doc and page -> del
    # check the text -> check_text
    # define the full paths -> pathlib.Path().resolve(), pathlib.PurePath().parent
    # rename the file -> os.rename()
    doc_to_extr = fitz.open(path_file_full)
    page_to_extr = doc_to_extr.load_page(0)

    page_bounds = get_page_bound_pdf(path_file_full)
    pdf_format_file = get_format(page_bounds[2], page_bounds[3])
    coord_rect_tuple = get_rectangle_extr(pdf_format_file)
    print('page parent: ', page_to_extr.parent)
    rect_to_extract = fitz.Rect(coord_rect_tuple)
    print('rect_to_extract: ', rect_to_extract)
    # doc_to_extr = get_doc(path_file_full)
    # page_to_extr = get_page(path_file_full)
    text_extr = page_to_extr.get_textbox(coord_rect_tuple)
    print('text_extr: ', text_extr)

    # to avoid any problems with objects, links, etc.
    del doc_to_extr, page_to_extr

    text = text_correction.text_filtering(text_extr, words_to_find)

    if len(text) < 15:
        print('The name is incorrect. Pay attention on it')
        list_bad_names.append(text)

    new_name = text + TYPE_FILE_SUFFIX
    new_name_full = pathlib.PurePath(path_file_full).parent / new_name
    old_name_full = pathlib.Path(path_file_full).resolve()
    os.rename(old_name_full, new_name_full)
    print('Success.')

    return new_name_full


# def check_path_dir: path()/str() -> bool)
# def check_text: str(), list[str(), str()] ->  bool()
# def check_path_file: path()/str() -> bool)
# def get_page_bound_pdf: path() -> list[int(), int()]
# def get_format: list[int(), int()] -> str()
# def get_rectangle_extr: str() -> fitz.Rect()
# def dir_content_pdf: path() -> list[str(), str()]
# def main_one_file: path() -> void()
def main():
    input_user = input('Type the full path to the directory: ')
    # check if the path is proper:
    if not check.check_path_dir(input_user):
        raise Exception()

    path_dir_full = pathlib.Path(input_user).resolve()
    os.chdir(path_dir_full)
    # list of filenames after renaming
    # get all pdf files in the directory
    content_list = dir_content_specified(path_dir_full)

    # for string in content_list:
    #     file_content = path_dir_full / string
    #     res_for_one_file = main_one_file(file_content)
    #     list_new_names.append(res_for_one_file)
    
    list_new_names = [main_one_file(path_dir_full / string) for string in content_list]

    print('Bad names: ', *list_bad_names)
    print('New names', *list_new_names)

    ans = 'Good work'
    return ans


if __name__ == '__main__':
    main()
