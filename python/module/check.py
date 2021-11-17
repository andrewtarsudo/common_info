import pathlib
import os


# path_dir - full path to the directory of str() or Path() type
# output - the value True/False of bool() type
# verify the correctness
def check_path_dir(path_dir: str) -> bool:
    path_dir_full = pathlib.Path(path_dir).resolve()
    # check the interruption
    if path_dir_full == '_exit_':
        raise InterruptedError
    # check the path follows to the directory
    if not path_dir_full.exists() and not path_dir_full.is_dir():
        print('The path is incorrect.')
        return False
    # check the access permissions
    try:
        os.access(path_dir_full, os.O_RDONLY)
    except PermissionError:
        print('It\'s not yours.')
        return False
    else:
        return True


# line - the symbols to check
# check_text - the words to check with
# output - the result of checks of bool() type
# do the check of the line, additional func for check_text
def check_line_start(line: str, check_text: list) -> bool:
    return any(line.startswith(word) for word in check_text)


# file_path - full path to the file of str() or Path() type
# output - the value True/False of bool() type
# verify the correctness
def check_path_file(file_path: str) -> bool:
    path_file = pathlib.Path(file_path).resolve()
    # check the interruption
    if file_path == '_exit_':
        raise InterruptedError
    # check the path follows to the file
    if not path_file.exists() and not path_file.is_file():
        print('The path is incorrect.')
        return False
    # check the access permissions
    try:
        os.access(file_path, os.O_RDONLY)
    except PermissionError:
        print('It\'s not yours.')
        return False
    else:
        return True
