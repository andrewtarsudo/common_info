import os
import pathlib
import fitz

#a4 595.2 x 841.69
#a3 1190.4 x 841.69
# const coordinates for the A4 file
UP_LEFT_X_A4 = 246
UP_LEFT_Y_A4 = 655
DOWN_RIGHT_X_A4 = 578
DOWN_RIGHT_Y_A4 = 697
# const coordinates for the A3 file
UP_LEFT_X_A3 = 833
UP_LEFT_Y_A3 = 658
DOWN_RIGHT_X_A3 = 1158
DOWN_RIGHT_Y_A3 = 700
# a list of the symbol combinations to search for
words_to_find = ['ПАМР', 'ПДРА']


# path_dir - full path to the directory of str() or Path() type
# output - the value True/False of bool() type
# verify the correctness 
def check_path_dir(path_dir):
    path_dir_full = pathlib.Path(path_dir).resolve()
    res = True

    if path_dir_full == '_exit':
        res = False
        raise InterruptedError
        return

    if not path_dir_full.exists():
        print('The path is incorrect.')
        res = False
        return

    if not path_dir_full.is_dir():
        print('The path specifies not a directory.')
        res = False
        return

    print(res)
    ans = res
    return ans


# text - the symbols extracted from the area of str() type
# output - the result of checks of bool() type
# do some checks for the text from the area
def check_text(text):
    if len(text) == 0:
        raise Exception('The text is not extracted.')
    #counter to find out if the words we need are extracted properly
    counter = 1
    for word in words_to_find:
        if text.startswith(word):
            # stop the program immediately when the match is found
            counter = 0
            break

    # the word is found
    if counter == 0:
        res = True
    # the word is not found
    elif counter == 1:
        res = False
    # smth strange happened
    else:
        raise Exception('You\'d better praise your sins. The elementary counter works badly.')

    print('text is ok?', res)
    ans = res
    return ans


def check_path_file(file_path):

    if file_path == '_exit':
        res = False
        raise InterruptedError
        return
    else:
        pass

    path_file = pathlib.Path(file_path).resolve()
    res = True

    if not path_file.exists():
        print('The path is incorrect.')
        res = False
        return
    else:
        pass

    if not path_file.is_file():
        print('The path specifies not a file.')
        res = False
        return
    else:
        pass

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
    print('result is ', ans)
    return res


# path_file - the full path to the file of str() or Path() type
# output - the first page of the file of Page() type
# get the page to analyze
def get_bound_pdf(path_file):
    print('type read_pdf', type(path_file))

    if path_file == '_exit_':
        print('The script is stopped.')
        raise InterruptedError('_exit_ is used to quit the program.')
    else:
        file_path = pathlib.Path(path_file).resolve()

    if not check_path_file(file_path):
        print('I\'m sorry.')
        return
    
    doc = fitz.open(file_path)
    print(type(file_path))
    doc_page = doc[0]
    # round the height and the width since it can be float but it's not good to compare numerics of different types
    print('doc_page', doc_page)
    rectangular = doc_page.irect
    point_tl = rectangular.top_left
    point_br = rectangular.bottom_right
    rect_height = rectangular.height
    rect_width = rectangular.width
    print('page bounds:', rectangular)

    ans = [rect_width, rect_height]
    return ans


def get_format(rect_width, rect_height):
    # define the most common formats
    if rect_height < 845 and rect_height > 835:
        if rect_width < 600 and rect_width > 590:
            format_file = 'A4'  # 595.2 x 841.69
        elif rect_width < 1195 and rect_width > 1185:
            format_file = 'A3'  # 1190.4 x 841.69
        else:
            # show the warning but continue operating
            format_file = 'UNKNOWN_FORMAT'
            print('The format is non-standard.')
    else:
        # show the warning but continue operating
        format_file = 'PAGE_SIZE_NOT_STANDARD'
        print('Page dimensions are unspecified.')

    ans = format_file
    print('format:', format_file)
    return ans


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
    rect_point_coord = {upleft_x, upleft_y, downright_x, downright_y}
    print('rectangle coordinates to extract:', rect_point_coord)

    ans = rectangle
    return ans


# formatFile - the typographic format A#: ..., A3, A4, A5, ...
# output - rectangle of Rect(x0, y0, x1, y1) type.
# define the rectangle
def main():
    input_user = str(input('Type the full path to the directory: '))
    input_path_dir = pathlib.Path(input_user).resolve()   
    # check if the path is proper:
    if not check_path_dir(input_user):
        raise Exception()
        return
    else:
        os.chdir(input_path_dir)

    # list of filenames after renaming
    list_new_names = []

    file_width, file_height = get_bound_pdf(input_path_dir)
    get_file_format = get_format(file_width, file_height)
    rect_to_extr = get_rectangle_extr(get_file_format)

    doc_to_extr = fitz.open(input_path_dir)
    page_to_extr = doc_to_extr.fullcopy_page(0)
    

main()
