import itertools
import pathlib
import codecs

replace_sym = ["\u201C", "\u201D"]


# def reading(path: pathlib.Path):
#     change = list()
#     with open(path, mode='r') as f:
#         for idx, line in enumerate(f):
#             change = [(idx, index) for index, sym in enumerate(line) if sym in replace_sym]
#     f.close()
#     print(change)
#     return change


# def replacing(path: pathlib.Path, change_list: list):
#     with open(path, mode='w') as f:
#         for item in change_list:
#             line = list(f)[item[0]],
#             str(line).replace(list(line)[item[1]], "\"")
#     f.close()
#     return None


def replace_symbol(path):
    with codecs.open(path, mode='rt') as file:
        text = file.readlines()
        # print(text)
        print(text)
        file.close()

    with codecs.open(path, mode='w') as f:
        for line in text:
            for sym in replace_sym:
                line.replace(sym, "\"")
        f.close()


def main():
    path_file = input('Type the path: ')
    path = pathlib.WindowsPath(path_file).resolve()
    work = 'not done'
    replace_symbol(path)
    work = 'done'
    print(f"The work is {work}")


if __name__ == '__main__':
    main()
