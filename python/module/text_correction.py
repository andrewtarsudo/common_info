import pathlib
import check

INDECES = {5, 6, 7, 8, 9, 10, 12, 13, 14}


def text_correction(path_file: str) -> str:
    path = pathlib.Path(path_file).resolve()
    name = list(pathlib.Path(path).name)

    if len(name) < 15:
        print('It\'s too short!')
        return ''.join(name)

    if not name[4] == '.':
        name.insert(4, '.')

    if not name[11] == '.':
        name.insert(11, '.')

    for index in INDECES:
        if name[index] == 'З':
            name[index] = '3'

        if name[index] == 'О':
            name[index] = '0'

    if len(name) > 16 and name[-1:-3] == 'СЬБ':
        del name[-2]

    if len(name) > 16 and name[-1:-2] == 'СЬ':
        name[-1] = 'Б'

    # converse the list to the string
    return ''.join(name)


# text - the symbols extracted from the area of str() type
# words_find - the list of searched symbols
# output - the result of checks of bool() type
# filter the text from the area to leave only needed part
def text_filtering(text: str, words_find: list) -> str:
    # index to extract the correct line
    index = -1
    for idx, value in enumerate(text.splitlines()):
        value.replace(' ', '')
        if check.check_line_start(value, words_find):
            index = idx
            return text_correction(value)

    if index == -1:
        raise Exception('The text is not extracted.')


def main():
    path = input('Type the path: ')
    text_correction(path)


if __name__ == '__main__':
    main()
