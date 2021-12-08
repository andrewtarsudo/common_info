import hashlib
import pathlib
import io

hash_algo = hashlib.md5()


def main():
    file_hash = input('Type the path to the file: ')
    path_file_hash = pathlib.Path(file_hash).resolve()

    with io.open(path_file_hash, 'r') as file:
        hash_algo.update(file)
        return hash_algo.hexdigest()


if __name__ == '__main__':
    main()
