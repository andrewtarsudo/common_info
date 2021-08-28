import os
import pathlib
import fitz
import pysvn

length_number = 18


# exist_oblige задает обязательность существования указанного пути


def full_path(file_path: str, exist_oblige: bool):
    path_file = pathlib.Path(file_path)
    while True:
        if path_file.exists():  # проверка существования, существует
            while True:
                if not path_file.is_file():  # указывает не на файл
                    path_file = input('It is not a file. Type the path again: ')
                else:  # получить абсолютный путь
                    path_file = path_file.resolve(strict=True)
                    break
            break
        else:  # проверка существования, не существует
            while True:
                if exist_oblige:  # обязан существовать
                    path_file = input('The file is not found. Type the new path: ')  # задать новый путь
                else:  # не обязан существовать
                    # создать директории, указанные в пути
                    print('The file is not found, but the folders are created.')
                    pathlib.Path.mkdir(parents=True)  # создаются все директории
                    break
            break

    ans = path_file
    return ans


def subst_name(old_name: str, new_name: str):  # подмена названия
    path_file_old = pathlib.Path.cwd() / old_name + '.pdf'  # старый путь
    path_file_new = pathlib.Path.cwd() / new_name + '.pdf'  # новый путь
    rename = path_file_old.rename(path_file_new)

    ans = pathlib.PurePath(rename).name  # название

    if ans != new_name:  # новое название совпадает с указанным
        print('Oh, my! You \'d better do something with it!')

    return ans


def pdf_extr(filename: str):  # извлечь текст из pdf
    path = pathlib.Path.cwd() / filename + '.pdf'  # путь из текущей папки + имя файла
    doc = fitz.open(path)  # открыть файл
    text = ''

    for page in doc:  # извлечь текст постранично
        text += page.getText()

    if text == '':  # если текст не удалось считать
        print('PDF text is not extracted. Change the fitz module to read the file.')

    ans = text
    return ans


def cut_str(text: str, args: list):  # разбить на подстроки
    sub_str = []  # массив подстрок

    for arg in args:
        start = 0  # индекс символа, с которого искать подстроку
        index = text.find(arg, start)  # индекс символа, с которого искать
        while index != -1:  # если найдено
            str_found = text[index:index + length_number - 1]  # вырезать часть
            text.append(str_found)  # добавить часть как новый элемент в конец
            start = index + length_number  # сдвинуть начало поиска
            index = text.find(arg, start)  # возврат к началу цикла while
        else:  # если не найдено или больше нет
            print("The search is finished.")
            break

    if len(sub_str) == 0:
        print("No substrings are found, you have made something wrong.")

    # проверка деления на подстроки, должно начинаться с ключевых слов
    for string in sub_str:
        counter = 0  # счетчик для проверки сразу по всем словам
        for arg in args:
            if string.startswith(arg) == str(arg):  # проверка первых букв
                counter += 1

        if counter == 1:
            print('At the time the things are ok')
        elif counter > 1:  # если начинается сразу с нескольких слов
            print('The counter is shitty. Make another one.')
        else:  # по идее, здесь только 0 остается
            print('The strings are incorrect or your counter is a POS.')

    ans = sub_str  # на вывод - массив найденных подстрок
    return ans


def find_str(text: string, find_words: list):  # поиск подстроки в тексте
    result_string = ""  # строка с найденными значениями
    indices = []  # индексы символов, с которых начинаются искомые подстроки

    for word in find_words:
        while True:
            index = text.find(word)  # индекс символа, с которого искать
            if index != -1:
                indices.append(index)  # фиксируем индекс начала подстроки
                text = text[index + length_number:]  # обрезаем текст
            else:
                print('The search is over.')
                break

    indices.sorted()  # сортируем индексы, чтобы они шли в порядке чтения
    # объединяем их все в строку, чтобы при дальнейших манипуляциях случайно не изменить их
    for index in indices:
        result_string += text[index:index + length_number - 1]

    ans = result_string  # на вывод - строка из найденных подстрок
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


def get_list_svn():  # получить список файлов из директории svn
    pysvn.Client.set_default_username('tarasov-a')  # логин для входа
    pysvn.Client.set_default_password('FXYfC6dh')  # пароль для входа
    result_find_words = []
    path = str(input('Type the path to the directory in svn. '))
    while True:  # проверка, является ли строкой
        if not pysvn.Client.is_url(path):
            print('The path is invalid. Try another one. ')
            path = str(input('The path is' ))
        else:
            break

    index = path.rfind('svn/')
    if index != -1:
        path = pathlib.Path('https://svn.protei.ru/svn/' + path[index + 4:])
        entry_list = pysvn.Client.ls(path)
        for entry in entry_list:
            result_find_words.append(entry.name)


def main_pdf():
    if os.name != 'Windows':
        print('Prepare for pain!')
    # переход в директорию с pdf
    pdf_dir = input('Type the path to the directory with the pamr/pdra pdf. ')
    path_pdf = full_path(pdf_dir, True)
    os.chdir(path_pdf)
    # открытие файла pdf и извлечение текста целиком
    pdf_name = input('Type the name of the pdf file with the pamr/pdra. ')
    path_pdf_name = full_path(pdf_name, True)
    pdra_pamr = pdf_extr(path_pdf_name)
    # поиск
    search_list = define_find_words()
    result_find_words = find_str(pdra_pamr, search_list)
    cut_str(result_find_words, search_list)
    # переход в директорию со скан-файлами
    scan = input('Type the path to the directory with the scanned docs. ')
    path_scan = full_path(scan, True)
    os.chdir(path_scan)
    # сортировка файлов по имени
    child_files = os.listdir(path_scan)
    new_scan = input('Type the path to the directory to store the new files. ')
    path_new_scan = full_path(new_scan, False)
    # перенос файлов в директорию для переименованных pdf
    for sub_string in cut_str:
        index = cut_str.index(sub_string)
        name_old = pathlib.Path.cwd() / child_files[index] + '.pdf'
        name_new = pathlib.PurePath(path_new_scan) / sub_string + '.pdf'
        subst_name(name_old, name_new)

def main_svn():
    get_list_svn()
    # переход в директорию со скан-файлами
    scan = input('Type the path to the directory with the scanned docs. ')
    path_scan = full_path(scan, True)
    os.chdir(path_scan)
    # сортировка файлов по имени
    child_files = os.listdir(path_scan)
    new_scan = input('Type the path to the directory to store the new files. ')
    path_new_scan = full_path(new_scan, False)
    # перенос файлов в директорию для переименованных pdf
    for sub_string in cut_str:
        index = cut_str.index(sub_string)
        name_old = pathlib.Path.cwd() / child_files[index] + '.pdf'
        name_new = pathlib.PurePath(path_new_scan) / sub_string + '.pdf'
        subst_name(name_old, name_new)


def main():
	while True:
		type = int(input('1-pdf, 0-svn'))
		if type == 1 or type == 0:
			break
		else:
			print('Wrong input.')
			type = int(input('1-pdf, 0-svn'))

	if type == 1:
		main_pdf()
	elif type == 0:
		main_svn()


main()
