import hashlib
import pathlib


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


def main():
    file_path_input = input('Path to the file:\n')
    # get the absolute path
    file_path = pathlib.Path(file_path_input).resolve()

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
    except Exception as e:
        print(f'The error {e.__class__.__name__} occurred.')
    except BytesWarning as w:
        print(f'The BytesWarning {w.__class__.__name__} has been raised.')
    else:
        print(f'The checksum is {get_md5(file_path)}.')

        close_input = input('Close the file? Y/N\n')

        while True:
            if close_input.upper() == 'N':
                continue
            elif close_input.upper() == 'Y':
                exit()
            else:
                print('Incorrect input.')
