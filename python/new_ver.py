import os
import pathlib
import fitz
import numpy


#a4 595.2 x 841.69
#a3 1190.4 x 841.69
# const coordinates for the A4 file
UP_LEFT_X_A4 = 250
UP_LEFT_Y_A4 = 650
DOWN_RIGHT_X_A4 = 600
DOWN_RIGHT_Y_A4 = 750
# const coordinates for the A3 file
UP_LEFT_X_A3 = 750
UP_LEFT_Y_A3 = 600
DOWN_RIGHT_X_A3 = 1200
DOWN_RIGHT_Y_A3 = 750
# a list of the symbol combinations to search for
words_to_find = ['ПАМР', 'ПДРА']


# path_dir - full path to the directory of str() or Path() type
# output - the value True/False of bool() type
# verify the correctness 
def check_path_dir(path_dir):
    path_dir_full = pathlib.Path(path_dir).resolve()
    res = True
    # check the interruption
    if path_dir_full == '_exit':
        res = False
        raise InterruptedError
        return
    else:
        pass
    # check the existance
    if not path_dir_full.exists():
        print('The path is incorrect.')
        res = False
        return
    else:
        pass
    # check the path follows to the directory
    if not path_dir_full.is_dir():
        print('The path specifies not a directory.')
        res = False
        return
    else:
        pass
    # check the access permissions
    try:
        os.access(path_dir_full, os.O_RDONLY)
    except PermissionError:
        print('It\'s not yours.')
        res = False
        return 
    else:
        pass
    finally:
        print('result is', res)

    ans = res
    return ans


# line - the symbols to check
# check_text - the words to check with
# output - the result of checks of bool() type
# do the check of the line, additional func fot check_text
def check_line_start(line, check_text):
    res = False

    for word in check_text:
        if line.startswith(word):
            res = True
            break
    
    return res


# text - the symbols extracted from the area of str() type
# words_find - the list of searched symbols
# output - the result of checks of bool() type
# filter the text from the area to leave only needed part
def text_filtering(text, words_find):
    text_list = text.splitlines()
    # index to extract the correct line
    index = -1

    for i in range(len(text_list)):
        if check_line_start(text_list[i], words_find):
            index = i
            res = True
            break

    if index == -1:
        raise Exception('The text is not extracted.')

    text = text_list[index].strip()
    print(text)

    ans = text
    return ans


# file_path - full path to the file of str() or Path() type
# output - the value True/False of bool() type
# verify the correctness 
def check_path_file(file_path):
    path_file = pathlib.Path(file_path).resolve()
    res = True
    # check the interruption
    if file_path == '_exit':
        res = False
        raise InterruptedError
        return
    else:
        pass
    # check the existance
    if not path_file.exists():
        print('The path is incorrect.')
        res = False
        return
    else:
        pass
    # check the path follows to the directory
    if not path_file.is_file():
        print('The path specifies not a file.')
        res = False
        return
    else:
        pass
    # check the access permissions
    try:
        os.access(file_path, os.O_RDONLY)
    except PermissionError:
        print('It\'s not yours.')
        res = False
        return 
    else:
        pass
    finally:
        print('result is ', res)

    ans = res
    return ans


# path_pdf_file - full path to the file of Path() type
# output - the parameters of list() with width of int type and height of int() type
# get the page amd its dimensions to analyze

def get_doc(path_pdf_file):
    doc = fitz.Document(path_pdf_file)

    ans = doc
    return ans


def get_page(path_pdf_file):
    doc = fitz.open(path_pdf_file)
    page = doc.load_page(0)

    ans = page
    return ans


def get_page_bound_pdf(path_pdf_file):
    doc = fitz.open(path_pdf_file)
    page_file_pdf = doc.load_page(0)
    # round the height and the width since it can be float but it's not good to compare numerics of different types
    Rect = page_file_pdf.rect
    iRect = Rect.irect 
    iRect_tl = iRect.top_left
    iRect_br = iRect.bottom_right
    
    iRect_width = iRect.width
    iRect_height = iRect.height

    ans = (iRect_tl, iRect_br, iRect_width, iRect_height)
    return ans


# rect_width and rect_height - the width and the height of the page of int() type
# output - the page format of str() type
# define the format
def get_format(rect_width, rect_height):
    # define the most common formats
    page_sizes = (int(rect_width), int(rect_height))
    print(rect_width, rect_height)
    print(fitz.paper_size('A3'))
    
    for index in range(0,1):
        print(numpy.abs(page_sizes[index] - fitz.paper_size('A4')[index]))
        print(numpy.abs(page_sizes[index] - fitz.paper_size('A3')[1-index]))
        
        if numpy.abs(page_sizes[index] - fitz.paper_size('A4')[index]) <= 2:
            format_file = 'A4'  # 595.2 x 841.69.
            
        elif numpy.abs(page_sizes[index] - fitz.paper_size('A3')[1-index]) <= 2:
            format_file = 'A3'  # 1190.4 x 841.69
            
        else:
            # show the warning but continue operating
            format_file = 'PAGE_SIZE_NOT_STANDARD'
            print('Page dimensions are unspecified.')
    
    print('format:', format_file)
    ans = format_file
    return ans


# formatFile - the typographic format A#: ..., A3, A4, A5, ... of str() type
# output - rectangle of fitz.Rect() type
# define the rectangle
def get_rectangle_extr(formatFile):
    # format A4, the common sheet
    if formatFile == 'A4':
        upleft_x = UP_LEFT_X_A4
        upleft_y = UP_LEFT_Y_A4
        downright_x = DOWN_RIGHT_X_A4
        downright_y = DOWN_RIGHT_Y_A4
    # format A3, two common sheets
    elif formatFile == 'A3':
        upleft_x = UP_LEFT_X_A3
        upleft_y = UP_LEFT_Y_A3
        downright_x = DOWN_RIGHT_X_A3
        downright_y = DOWN_RIGHT_Y_A3
    # another format, input its width and height
    else:
        upleft_x = 0
        upleft_y = 0
        downright_x = DOWN_RIGHT_X_A3
        downright_y = DOWN_RIGHT_Y_A3

    # construct Rect() rectangle
    rect_point_coord = (upleft_x, upleft_y, downright_x, downright_y)
    print('rectangle coordinates to extract:', *rect_point_coord)

    ans = rect_point_coord
    return ans


# path_to_dir - the full path to the directory with pdf files of str() or Path() type
# output - the list of the files with *.pdf extension inside the directory of list() type with items of Path() type
# get the specific contents of the directory
def dir_content_pdf(path_to_dir):
    full_content = os.listdir(path_to_dir)
    spec_content = []

    for file in full_content:
        # transform needed strings to paths of Path() type
        if pathlib.PurePath(file).suffix == '.pdf':
            spec_content.append(pathlib.Path(file).resolve())

    ans = spec_content
    return ans


# path_file_full - path to the file of path() type
# output - void
# the main activity for one file
def main_one_file(path_file_full):
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
    print('type doc_to_extr: ', type(doc_to_extr))
    print('type page_to_extr: ', type(page_to_extr))
    print('page parent: ', page_to_extr.parent)
    rect_to_extract = fitz.Rect(coord_rect_tuple)
    print('rect_to_extract: ', rect_to_extract)
    # doc_to_extr = get_doc(path_file_full)
    # page_to_extr = get_page(path_file_full)
    text_extr = page_to_extr.get_textbox(coord_rect_tuple)
    print('text_extr: ', text_extr)

    # to avoid any problems with objects, links, etc.
    del doc_to_extr, page_to_extr
    
    text = text_filtering(text_extr, words_to_find)
    
    new_name = text + '.pdf'
    new_name_full = pathlib.PurePath(path_file_full).parent / new_name
    old_name_full = pathlib.Path(path_file_full).resolve()
    os.rename(old_name_full, new_name_full)
    print('Success.')
    
    ans = new_name_full
    return ans
    
    
# def check_path_dir: path()/str() -> bool)
# def check_text: str(), list[str(), str()] ->  bool()
# def check_path_file: path()/str() -> bool)
# def get_page_bound_pdf: path() -> list[int(), int()]
# def get_format: list[int(), int()] -> str()
# def get_rectangle_extr: str() -> fitz.Rect()
# def dir_content_pdf: path() -> list[str(), str()]
# def main_one_file: path() -> void()
def main():
    input_user = str(input('Type the full path to the directory: '))
    # check if the path is proper:
    if not check_path_dir(input_user):
        raise Exception()
        return

    path_dir_full = pathlib.Path(input_user).resolve()
    os.chdir(path_dir_full)
    # list of filenames after renaming
    list_new_names = []
    # get all pdf files in the directory
    content_list = dir_content_pdf(path_dir_full)

    for string in content_list:
        file_content = path_dir_full / string
        res_for_one_file = main_one_file(file_content)
        list_new_names.append(res_for_one_file)

    ans = 'Good work'
    return ans

main()
