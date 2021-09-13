import os
import pathlib
import fitz


# old_name - старое название файла с расширением
# old_name_path - путь до старого файла
# new_name - новое название файла с расширением
# new_name_path - путь до нового файла
def subst_name(old_name, old_name_path, new_name, new_name_path):  # подмена названия
    # старый путь
    path_file_old = pathlib.Path(old_name_path).resolve() / old_name
    # новый путь
    path_file_new = pathlib.Path(new_name_path).resolve() / new_name
    rename = path_file_old.rename(path_file_new)

    ans = pathlib.PurePath(rename).name()  # название
    return ans


# file_path - путь до директории с файлом
# filename - название файла с расширением
def text_extr(file_path, filename):  # извлечь текст
    path = pathlib.Path(file_path).resolve() / filename  # путь из текущей папки + имя файла c расширением
    full_path = pathlib.Path(path).resolve()
    text = ''  # будет хранить текст файла

    while True:
        # проверка корректности пути
        if not pathlib.Path(full_path).exists():
            print('The path is incorrect.')
            path = input('Type the full path: ')
            full_path = pathlib.Path(path).resolve()

    while True:
        # если pdf-файл
        if path.PurePath(full_path).suffix == '.pdf':
            doc = fitz.open(full_path)  # открыть файл
            # извлечь текст постранично
            for page in doc:  
                text += page.getText()

            break
        # если txt-файл из pdf
        elif path.PurePath(full_path).suffix == '.txt':
            try:
                # проверяем права доступа
                doc = os.open(full_path, 'rt')
                # извлечь текст постранично
                for line in doc:
                    text += line + ' '
                break
            # ошибка прав доступа
            except OSError:
                print('The problem to open in the read-write mode.')
                break
        # если путь указан лишь до директории
        elif path.PurePath(full_path).suffix == '':
            print('Type the correct path to the file.')
            file_path = input('The path is: ')
            path = pathlib.Path(file_path).resolve() / filename  # путь из текущей папки + имя файла
            full_path = pathlib.Path(path).resolve()
        # вариант файла другого формата
        else:
            print("The correct file types are *.txt and *.pdf.")
            raise Exception("Choose another file.")

    # если текст не удалось считать
    if len(text) == 0:  
        print('PDF text is not extracted. Change the fitz module to read the file.')
    # разбиение строки на список строк по пробелу
    list_text = text.split('')

    ans = list_text
    return ans


# text - строка с текстом
# find_words - список искомых слов
def find_str(text, find_words):  # поиск подстроки в тексте
    list_ok = []  # список, куда будут записаны нужные подстроки

    for string in text:
        for word in find_words:
            if string.startswith(word):
                list_ok.append(string)
                text.remove(string)
            else:
                text.remove(string)

    # на вывод - строка из найденных подстрок
    ans = list_ok  
    return ans


def define_find_words():  # задать ключевые слова для поиска
    words_find = []  # список, куда записываем нужные слова
    while True:
        word = str(input('Type the key word to look for. Push the Enter key to leave. If you made a mistake, you will have a chance to change them, do not worry. '))
        # условие выхода - пустая строка
        if word == '': 
            print('You finished entering the words.')
            print(*words_find)
            break
        else:
            words_find.append(word)

    ans = words_find
    return ans


# проверка на пустой ввод
def input_empty(input_string, list_values):
    if isinstance(list_values, list):
        if input_string == '' or input_string.startswith(' '):
            list_values.remove(input_string)
            ans = None
        else:
            ans = input_string

    return ans


def check_change_list_input(list_words):  # узнаем, хотим ли вообще что-то делать
    glob_ans_change = str(input('Do you want to do something with words?'))

    if glob_ans_change == 'y' or glob_ans_change.casefold() == 'yes':
        print("Oh, really? Ok, let's do some work.")
        print('Choose the action to do: add(), change(), delete(). Choose your destiny! ')
        answer = str(input())

        if answer == 'add()':
            add_find_words(list_words)

        elif answer == 'change()':
            change_find_words(list_words)

        elif answer == 'delete()':
            delete_find_words(list_words)
            
        else:
            pass

    else:
        print("Ok, let's go next!")


# list_words - список со словами
def add_find_words(list_words):  # добавить ключевое слово для поиска
    print('You can add only one words at time. Type _exit_ to add nothing and return to other actions.')
    add_word = str(input('Type the word to add: '))
    # проверка на выход
    if add_word == '_exit_':
        print("Ok, let's return back.")
    # добавление слова
    else:
        list_words.append(add_word)
        print('The word %s is added.'%add_word)

    ans = list_words
    # возвращаемся в меню
    check_change_list_input(list_words)
    return ans


# list_words - список со словами
def delete_find_words(list_words):  # удалить ключевое слово для поиска
    print('You can delete only one words at time. Type _exit_ to delete nothing and return to other actions.')
    delete_word = str(input('Type the word to delete: '))
    # проверка на выход
    if delete_word == '_exit_':
        print("Ok, let's return back.")
    # удаление слова
    else:
        try:
            list_words.remove(add_word)
            print('The word %s is deleted.'%add_word)
        except ValueError:
            print('There is no such word.')

    ans = list_words
    # возвращаемся в меню
    check_change_list_input(list_words)
    return ans

# list_words - список со словами
def change_find_words(list_words):  # изменить ключевые слова для поиска
    for item in list_words:
        print('Do you want to change the word %s? y/n'%item)
        user_input = str(input())
        # проверка на выход
        if user_input == '_exit_':
            print("Ok, let's return back.")
        # если слово надо изменить
        elif user_input.casefold() == 'y' or user_input.casefold() == 'yes':
            print('Well, ok. Type _exit_ to change nothing and return to other actions.')
            index = list_words.index(item)
            user_word_add = str(input('Push Enter to change nothing. Type the new word: '))
            # проверка на пустой ввод
            if user_word_add == '':
                print('No changes are made, %s.'%list_words[index])
            else:
                list_words[index] = user_word_add
                print('The new word is %s.'%user_word_add)
        # если слово не надо менять
        else:
            print("Great! Let's go next.")

    ans = list_words
    check_change_list_input(list_words)

    return list_words


# file_location — файл, откуда брать ПАМР/ПДРА
# file_dir — директория file_location
# file_real_name — название файла
# key_words — список искомых ключевых слов
# extracted_text — полученный текст
# list_proper — извлеченные номера

# subst_name(old_name, old_name_path, new_name, new_name_path) -> name
# def text_extr(file_path, filename) -> text list
# def find_str(text, find_words) -> list pamr/pdra numbers
# def define_find_words() -> None


def main():
    # переход в директорию с pdf
    file_location = input('Type the path to the directory with the file: ')
    temp = pathlib.Path(file_location).resolve()
    file_dir = pathlib.PurePath(temp).parent
    file_real_name = pathlib.PurePath(temp).name
    # работа с ключевыми словами поиска
    key_words = define_find_words()
    change_find_words(key_words)
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

    # перечень наименований в директории со старыми файлами
    ins = os.listdir(old_files)  # 
    content = []

    # выделить только сканы, вдруг еще есть другие файлы
    for file in ins:
        if file.endswith('.pdf'):
            content.append(file)

    # проверка длин списка со старыми названиями и новыми названиями
    if len(content) == len(numbers_proper):
        print('Everything is ok.')
    else:
        print('The number of files and the number of found strings are different. Check the program.')
        to_continue = str(input('Do you want to continue despite the difference? y/n'))
        while True:
            if to_continue.casefold() == 'yes' or to_continue.casefold() == 'y' or to_continue.casefold() == 'да' or to_continue.casefold() == 'д' or to_continue.casefold() == 'lf' or to_continue.casefold() == 'da':
                print('You decide to continue. Ok.')
                break
            elif to_continue.casefold() == 'no' or to_continue.casefold() == 'n' or to_continue.casefold() == 'нет' or to_continue.casefold() == 'н' or to_continue.casefold() == 'ytn' or to_continue.casefold() == 'net':
                print('You decided to stop. Terminating the script...')
                raise Exception('The list sizes are not the same.')
            else:
                print('I do not understand you. Try one more time.')
                print("'yes', 'y', 'да', 'д', 'lf', 'da', 'no', 'n', 'нет', 'н', 'ytn', 'net' are acceptable.")
                to_continue = str(input('Do you want me to do the script next? y/n'))

    # переименование
    for index in range(0, len(content)):
        subst_name(content[index], old_files, numbers_proper[index], new_files)

    ans = None
    return ans

main()
