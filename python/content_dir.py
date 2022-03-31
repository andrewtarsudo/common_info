import pathlib


def main():
    pathfile = input('Path to the directory:\n')
    
    try:
        path = pathlib.Path(pathfile).resolve(strict=True)
        for item in path.iterdir():
            print(item.name)
    except NotADirectoryError as e:
        print(f"Error {e.errno} in line {e.__traceback__.tb_lineno}. It's not a directory.")
    except FileNotFoundError as e:
        print(f"Error {e.errno} in line {e.__traceback__.tb_lineno}. The specified directory doesn't exist.")
    except TypeError as e:
        print(f'TypeError in line {e.__traceback__.tb_lineno}. The path is incorrect.')
    except PermissionError as e:
        print(f'Error {e.errno} in line {e.__traceback__.tb_lineno}. You have no permission to access the directory.')
    except OSError as e:
        print(f'OSError {e.errno} in line {e.__traceback__.tb_lineno}.')


if __name__ == '__main__':
    main()
