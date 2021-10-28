import pathlib


def main():
    pathfile = input('Path to the directory: ')
    path = pathlib.Path(pathfile).resolve()

    if pathlib.Path(path).is_dir():
        for item in pathlib.Path(path).iterdir():
            print(item.name)
    else:
        print('Failed. Sorry')


main()
