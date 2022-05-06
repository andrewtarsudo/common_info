from pathlib import Path
from pprint import pprint
from typing import Union
from os import chdir


def _check_path(path_dir: Union[str, Path]):
    try:
        chdir(Path(path_dir).resolve(True))
    except PermissionError:
        raise PermissionError(f"Not enough access rights for {path_dir}.")
    except AttributeError:
        raise AttributeError(f"The path {path_dir} is not correct.")
    except RuntimeError:
        raise RuntimeError(f"Waiting timeout of the system response for moving to the {path_dir} directory. The most "
                           f"probable cause: infinite loop.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The directory {path_dir} doesn't exist.")
    except OSError as e:
        raise OSError(f"The error {e.errno} occurred. {e.strerror}")
    else:
        if not Path(path_dir).resolve(True).is_dir():
            raise NotADirectoryError(f"The path {path_dir} doesn't point to the directory.")
        else:
            return True


def get_content_dir(path_dir: Union[str, Path]):
    if _check_path(path_dir):
        path = Path(path_dir).resolve()
        return [item for item in Path(path).iterdir()]



def main():
    path = input('Path to the directory:\n')
    pprint(get_content_dir(path))


if __name__ == '__main__':
    main()
