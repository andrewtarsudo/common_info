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
        upleft_x = 0
        upleft_y = 0
        downright_x = DOWN_RIGHT_X_A3
        downright_y = DOWN_RIGHT_Y_A3

    # construct Rect() rectangle
    rectangle = fitz.Rect(upleft_x, upleft_y, downright_x, downright_y)
    print('rectangle to extract: ', rectangle)

    ans = rectangle
    return ans


# path_file - the full path to the file of str() or Path() type
# output - the first page of the file of Page() type
# get the page to analyze
def read_pdf(path_file):
    while True:
        if path_file == '_exit_':
            print('The script is stopped.')
            raise InterruptedError('_exit_ is used to quit the program.')
        else:
            file_path = pathlib.Path(path_file).resolve()

            try:
                # open the file
                doc = fitz.open(file_path)
                print('doc type:', type(doc))
            except FileNotFoundError:
                print('You fucked up. Type the real path to the real pdf file.')
            except IsADirectoryError:
                print('Type the path to the file up to the end.')
            except PermissionError:
                print('You have no access to the file. Do smth with it.')
            else:
                # extract the first page, interrupt the loop
                doc_page = doc.load_page(0)
                print('doc_page Type:', type(doc_page))
                break

    ans = doc_page
    return ans


# page_pdf - the page of the document of Page() type
# output - the format of the page of str() type. A3 and A4 are specified
# determine the page format
def file_format(page_doc):
    # round the height and the width since it can be float but it's not good to compare numerics of different types
    rectangular = page_doc.bound()
    print('page bounds:', rectangular)
    lRect_page = rectangular.round()
    print('rounded page bounds:', lRect_page)
    
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
    if lRect_page.height < 845 and lRect_page.height > 835:
        if lRect_page.width < 600 and lRect_page.width > 590:
            format = 'A4'  # 595.2 x 841.69
        elif lRect_page.width < 1195 and lRect_page.width > 1185:
            format = 'A3'  # 1190.4 x 841.69
        else:
            # show the warning but continue operating
            format = 'UNKNOWN_FORMAT'
            raise Warning('The format is non-standard.')
    else:
        # show the warning but continue operating
        format = 'PAGE_SIZE_NOT_STANDARD'
        raise Warning('Page dimensions are unspecified')

    ans = format
    print('format:', format)
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

    print(*spec_content)
    ans = spec_content
    return ans


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

    priint(res)
    ans = res
    return ans


# path_dir - full path to the file of str() or Path() type
# output - the value True/False of bool() type
# verify the correctness 
def check_path_file(path_file):
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

    if not path_dir_full.is_file():
        print('The path specifies not a file.')
        res = False
        return

    print(res)
    ans = res
    return ans


# def rectangle_extr(formatFile) -> fitz.Rect()
# def file_format(page) -> str()
# def read_pdf(file_path) -> fitz.Page()
# def check_text(text) -> bool()
# def dir_content_pdf(path_to_dir) -> list() of pathlib.PurePath()
def main():
    input_user = str(input('Type the full path to the directory: '))
    print(input_user)
    input_path_dir = pathlib.Path(input_user).resolve()   
    # check if the path is proper:
    if not check_path_dir(input_user):
        raise Exception()
        return
    else:
        os.chdir(input_path_dir)

    # list of filenames after renaming
    list_new_names = []

    for file in dir_content_pdf(pathlib.Path.cwd()):
        print(file)
        pdf_file_page = read_pdf(pathlib.Path.cwd() / file)
        print(type(pdf_file_page))
        format_pdf = file_format(pdf_file_page)
        print(format_pdf)
        rect = rectangle_extr(format_pdf)
        # rect - fitz.Rect()
        # output - str()
        extr_text = pdf_file_page.get_textbox(rect)
        print(extr_text)
        
        # check the text from the pdf
        if check_text(extr_text):
            new_name_full = extr_text + '.pdf'
            os.rename(pathlib.Path.cwd() / file, pathlib.Path.cwd() / new_name_full)
            list_new_names.append(new_name_full)
            print('Success.')
            print(new_name_full)
        # if the text fails
        else:
            print('The text is incorrect.')
            list_new_names.append('FAILED')

    ans = list_new_names
    return ans


main()
