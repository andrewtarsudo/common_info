import os
import pathlib
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

# a list of the symbol combinations to search for
words_to_find = ['ПАМР', 'ПДРА']

# formatFile - the typographic format A#: ..., A3, A4, A5, ...
# output - rectangle of Rect(x0, y0, x1, y1) type.
# define the rectangle
def rectangle_extr(formatFile):
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
        try:
            downright_x_input = int(input('Type the width in px: '))
            downright_y_input = int(input('Type the height in px: '))
        except TypeError:
            # improper input
            print('The input is incorrect')
            downright_x = -1
            downright_y = -1
        else:
            # use abs in case of the negative numbers due to bqad calculations
            upleft_x = 0
            upleft_y = 0
            downright_x = abs(downright_x_input)
            downright_y = abs(downright_y_input)

    # construct Rect() rectangle
    rectangle = fitz.Rect(upleft_x, upleft_y, downright_x, downright_y)

    ans = rectangle
    return ans


# file_path - the full path to the file of str() or Path() type
# output - the first page of the file of Page() type
# get the page to analyze
def read_pdf(file_path):
    while True:
        if file_path == '_exit_':
            print('The script is stopped.')
            raise InterruptedError('_exit_ is used to quit the program.')
        else:
            file_path = pathlib.Path(file_path).resolve()

            try:
                doc = fitz.open(file_path)  # type fitz.Document
            except FileNotFoundError:
                print('You fucked up. Type the real path to the real pdf file.')
            except IsADirectoryError:
                print('Type the path to the file up to the end.')
            except PermissionError:
                print('You have no access to the file. Do smth with it.')
            else:
                # extract the first page and close the file, intrerrupt the loop while
                doc_page = doc.load_page(0)  # type fitz.Page
                break
            finally:
                print(type(doc))

    ans = doc_page
    print(type(ans))
    return ans


# page_pdf - the list from the document of Page() type
# output - the format of the page of str() type. A3 and A4 are specified
# determine the page format
def file_format(file_path):
    doc = fitz.open(pathlib.Path(file_path).resolve())
    pdf_page = doc.load_page(0)
    print(file_path)
    print(type(pdf_page))
    
    # round the height and the width since it can be float but it's not good to compare numerics of different types
    Rectangular = pdf_page.bound()
    # print(Rectangular)
    lRect_page = Rectangular.round()
    # check if the rectangle becomes an interval
    if lRect_page.is_empty:
        print('You have some problems. I\'m sorry.')
    #check if the rectangle is infinite, {x0, x1} and {y0, y1} are messed
    #modify the rectangle if it's infinite
    if lRect_page.is_infinite:
        lRect_page.normalize()

    print('width = ', lRect_page.width)
    print('height = ', lRect_page.height)
    # define the most common formats
    if lRect_page.height < 850 and lRect_page.height > 840:
        if lRect_page.width < 590 and lRect_page.width > 600:
            format = 'A4'  # 794 x 1123
        elif lRect_page.width < 1580 and lRect_page.width > 1590:
            format = 'A3'  # 1587 x 1123
        else:
            # show the warning but continue operating
            format = 'UNKNOWN_FORMAT'
            raise Warning('The format is non-standard.')
    else:
        # show the warning but continue operating
        format = 'PAGE_SIZE_NOT_STANDARD'
        raise Warning('Page dimensions are unspecified')

    ans = format
    print(format)
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
            res = 0
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

    ans = res
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


# def rectangle_extr(formatFile) -> fitz.Rect()
# def file_format(page) -> str()
# def read_pdf(file_path) -> fitz.Page()
# def check_text(text) -> bool()
# def dir_content_pdf(path_to_dir) -> list() of pathlib.PurePath()
def main():
    input_user = input('Type the full path to the directory: ')
    input_path_dir = str(input_user)
    print(input_user)
    print(type(input_user))
    # input_path_dir = str('C:\Users\tarasov-a\Desktop\Testing')
    #check for interruption
    if input_path_dir == '_exit':
        raise InterruptedError

    # check if the path is proper:
    try:
        path_dir = pathlib.Path(input_path_dir).resolve()
    except PermissionError:
        print('You have no access, pos.')
        return
    except InterruptedError:
        print('It was your choice. It\'s not my fault.')
        return
    except FileNotFoundError:
        print('The path is incorrect.')
    else:
        pass
    list_new_names = []

    for scan in dir_content_pdf(path_dir):
        print(scan)
        pdf_scan_page = read_pdf(path_dir.joinpath(scan))
        print(type(pdf_scan_page))
        format = file_format(path_dir.joinpath(scan))
        print(format)
        rect = rectangle_extr(format)
        # rect - fitz.Rect()
        # output - str()
        extr_text = pdf_scan_page.get_textbox(rect)
        print(extr_text)
        # check the text from the pdf
        if check_text(extr_text):
            new_name_full = extr_text + '.pdf'
            os.rename(scan, path_dir.joinpath(new_name_full))
            list_new_names.append(new_name_full)
            print('Success.')
            
        else:
            raise Warning('The text is incorrect.')
            list_new_names.append('%s failed'%scan.suffix)


    ans = list_new_names
    return ans


main()
