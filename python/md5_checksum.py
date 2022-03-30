import hashlib
import pathlib


def verify_path(file_path: pathlib.Path) -> bool:
    """
    Checks the file path input.\n
    :param file_path: the path to file, pathlib.Path
    :return: the verification flag of the bool type.
    """
    flag_verify = False
    try:
        with open(file_path, "rb") as file:
            file.close()
    except FileNotFoundError as e:
        print(f'The FileNotFoundError {e.__class__.__name__} occurred since the file does not exist.')
    except PermissionError as e:
        print(f'The PermissionError {e.__class__.__name__} occurred since you have not enough permissions.')
    except RuntimeError as e:
        print(f'The RuntimeError {e.__class__.__name__} occurred since the program works too long.')
    except OSError as e:
        print(f'The OSError {e.__class__.__name__} occurred.')
    except BytesWarning as w:
        print(f'The BytesWarning {w.__class__.__name__} has been raised.')
    except Exception as e:
        print(f'The error {e.__class__.__name__} occurred.')
    else:
        flag_verify = True
        print('The file is ok.')
    finally:
        return flag_verify


def get_md5(path_file: pathlib.Path) -> str:
    """
    Gets the MD5 hash of the file.\n
    :param path_file: the path to file, str
    :return: the MD5 checksum in the hex format of the str type.
    """
    hash_md5 = hashlib.md5()
    with open(path_file, "rb") as file:
        # cut the file into the pieces of the 4096 bits
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)

    md5_checksum = hash_md5.hexdigest()
    file.close()
    return md5_checksum


def verify_checksum(md5_checksum: str):
    """
    Compares the result with the OM-specified checksum.\n
    :param md5_checksum: the received result of the hex format, str
    :return: None.
    """
    om_checksum = input('The developer checksum:\n')
    if md5_checksum == om_checksum:
        print('The checksums are equal.')
    else:
        print('The checksums are different. Something went wrong.')


def write_checksum(md5_checksum: str):
    """
    Writes the received result to the file.\n
    :param md5_checksum: the received result of the hex format, str
    :return: None.
    """
    path_file_write = input('The path to the file to write:\n')
    try:
        with open(path_file_write, 'w+') as file:
            file.write(f'MD5 checksum = \n{md5_checksum}')
    except PermissionError as e:
        print(f'The PermissionError {e.__class__.__name__} occurred since you have not enough permissions.')
    except RuntimeError as e:
        print(f'The RuntimeError {e.__class__.__name__} occurred since the program works too long.')
    except OSError as e:
        print(f'The OSError {e.__class__.__name__} occurred.')
    finally:
        file.close()


def process_input(prompt: str, prompt_y: str = None, prompt_n: str = None, prompt_neither: str = None) -> bool:
    """
    Loops the input to get the Y string.\n
    :param prompt: the prompt before the user input, str
    :param prompt_y: the prompt for the Y input, str
    :param prompt_n: the prompt for the N input, str
    :param prompt_neither: the prompt for the inappropriate input, str
    :return: the flag to leave the loop, bool
    """
    while True:
        user_input = input(prompt)
        if user_input.upper() == 'N':
            if prompt_n is not None:
                print(prompt_n)
        elif user_input.upper() == 'Y':
            if prompt_y is not None:
                print(prompt_y)
            return True
        else:
            if prompt_neither is not None:
                print(prompt_neither)


def main():
    file_path_input = input('The path to the file:\n')
    # get the absolute path
    file_path = pathlib.Path(file_path_input).resolve()

    if not verify_path(file_path=file_path):
        print('The path is not proper. THe program is terminated.')
        exit()

    md5_checksum = get_md5(file_path)
    print(f'The checksum is {md5_checksum}.')

    print('Do you want to verify the checksum? Y/N')
    verify_input = input('Default: N.\n')

    if verify_input.upper() == 'Y':
        verify_checksum(md5_checksum)
    else:
        print('Do you want to save the checksum to the file? Y/N')
        write_input = input('Default: N.\n')
        if write_input == 'Y':
            write_checksum(md5_checksum=md5_checksum)

    if process_input(prompt='Close the file? Y/N\n', prompt_y=None, prompt_n=None, prompt_neither='Incorrect input.'):
        exit()


if __name__ == '__main__':
    main()
