import pathlib

list_content = []


def get_content_dir(pathfile):
    path = pathlib.Path(pathfile).resolve()

    if pathlib.Path(path).is_dir():
        for item in pathlib.Path(path).iterdir():
            list_content.append(item)
    else:
        print('Failed. Sorry')

    return list_content


def main():
    path = input('Path to the directory: ')
    print(get_content_dir(path))


if __name__ == '__main__':
    main()
