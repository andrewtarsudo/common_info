import os
import pathlib
import fitz


def subst_name(old_name, old_name_path, new_name, new_name_path):  # подмена названия
    # старый путь
    path_file_old = pathlib.Path(old_name_path).resolve() / old_name
    # новый путь
    path_file_new = pathlib.Path(new_name_path).resolve() / new_name
    rename = path_file_old.rename(path_file_new)
    ans = pathlib.PurePath(rename).name()  # название

    if ans != new_name:  # новое название совпадает с указанным
        print('Oh, my! You \'d better do something with it!')

    return ans


def text_extr(file_path, filename):  # извлечь текст
    path = pathlib.Path(file_path).resolve() / filename  # путь из текущей папки + имя файла
    full_path = pathlib.Path(path).resolve()
    text = ''

    while True:
        if not pathlib.Path(full_path).exists():
            print('The path is incorrect.')
            path = input('Type the full path: ')
            full_path = pathlib.Path(path).resolve()
            )

    while True:
        if path.PurePath(full_path).suffix == '.pdf':
            doc = fitz.open(full_path)  # открыть файл

            for page in doc:  # извлечь текст постранично
                text += page.getText()

            break

        elif path.PurePath(full_path).suffix == '.txt':
            try:
                doc = os.open(full_path, 'rt')
            except OSError:
                print('The problem to open in the read-write mode.')

            for line in doc:
                text += line + ' '

            break

        elif path.PurePath(full_path).suffix == '':
            print('Type the correct path to the file.')
            file_path = input('The path is: ')
            path = pathlib.Path(file_path).resolve() / filename  # путь из текущей папки + имя файла
            full_path = pathlib.Path(path).resolve()

        else:
            print("It's not real, the option is impossible.")
        
    if len(text) == 0:  # если текст не удалось считать
        print('PDF text is not extracted. Change the fitz module to read the file.')

    list_text = text.split("")
    
    ans = list_text
    return ans


def find_str(text, find_words):  # поиск подстроки в тексте
    list_ok = []  # индексы символов, с которых начинаются искомые подстроки

    for string in text:
        for word in find_words:
            if string.startswith(word):
                list_ok.append(string)
                text.remove(string)
            else:
                text.remove(string)

    ans = list_ok  # на вывод - строка из найденных подстрок
    return ans


def define_find_words():  # задать ключевые слова для поиска
    words_find = []
    while True:
        word = str(input('Type the key word to look for. Push the Enter key to leave. '))
        if word == '': # условие выхода - пустая строка
            print('You finished entering the words. ')
            print(*words_find)
            break
        else:
            words_find.append(word)

    ans = words_find
    return ans


# file_location — файл, откуда брать ПАМР/ПДРА
# file_dir — директория file_location
# file_real_name — название файла
# key_words — список искомых ключевых слов
# extracted_text — полученный текст
# numbers_proper — извлеченные номера
# old_files — директория для старых файлов
# new_files — директория для новых файлов
# ins — список содержимого директории old_files
# content — содержимое


# def subst_name(old_name, old_name_path, new_name, new_name_path) -> name
# def text_extr(file_path, filename) -> text list
# def find_str(text, find_words) -> list pamr/pdra numbers
# def define_find_words() -> None


def main():
    # переход в директорию с pdf
    file_location = input('Type the path to the directory with the file: ')
    temp = pathlib.Path(file_location).resolve()
    file_dir = pathlib.PurePath(temp).parent
    file_real_name = pathlib.PurePath(temp).name

    key_words = define_find_words()
    extracted_text = text_extr(file_dir, file_real_name)
    numbers_proper = find_str(extracted_text, key_words)

    old_files = input('Type the path to the dir with files to rename: ')
    new_files = input('Type the path to the dir with new files: ')

    while True:
        if not pathlib.Path(old_files).is_dir():
            print('Try again.')
            old_files = input('Type the path to the old files: ')
        elif not pathlib.Path(new_files).is_dir():
            print('Try again.')
            new_files = input('Type the path to the new files: ')
        else:
            break

    ins = os.listdir(old_files)  # 
    content = []

    for file in ins:
        if file.endswith('.pdf'):
            content.append(file)

    if len(content) == len(numbers_proper):
        print('Everything is ok.')
    else:
        print('The number of files and the number of found strings are different. Check the program.')
        to_continue = str(input('Do you want to continue despite the difference? y/n\n'))
        while True:
            if to_continue.casefold() == 'yes' or to_continue.casefold() == 'y' or to_continue.casefold() == 'да' or to_continue.casefold() == 'д' or to_continue.casefold() == 'lf':
                print('You decide to continue. Ok.')
                break
            elif to_continue.casefold() == 'no' or to_continue.casefold() == 'n' or to_continue.casefold() == 'нет' or to_continue.casefold() == 'н' or to_continue.casefold() == 'ytn':
                print('You decided to stop. Terminating the script...')
                raise Exception('The list sizes are not the same.')
            else:
                print('I do not understand you. Try one more time.')
                to_continue = str(input('Do you want me to do the script next? y/n'))
            
    for index in range(0, len(content)):
        subst_name(content[index], old_files, numbers_proper[index], new_files)

    ans = None
    return ans


main()
