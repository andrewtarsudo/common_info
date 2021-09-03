import json
import os
import sys
import pathlib
import pysvn
import tabula


def full_path(file_path: str):
    while True:
        try:
            path_file = pathlib.Path.resolve(file_path, strict = True)
            break
        except FileNotFoundError:
            file_path = input('The path is wrong. Try again: ')

    ans = path_file
    return ans


def subst_name(old_name: str, new_name: str):  # подмена названия
    path_file_old = pathlib.Path.cwd() / old_name + '.pdf'  # старый путь
    path_file_new = pathlib.Path.cwd() / new_name + '.pdf'  # новый путь
    rename = full_path(path_file_old).replace(full(path_file_new))

    ans = pathlib.PurePath(rename).name  # название
    if ans != new_name:  # новое название совпадает с указанным
        print('Oh, my! You \'d better make this thing rename the files!')
    elif Path(pathlib.Path(path_file_old).resolve()).exists():
        print('For the Fcking Sake, the old file in not deleted.')
    else:
        pass

    return ans


def pdf_extr(filename):  # извлечь текст из pdf
    file_name = filename + '.pdf'
    path = pathlib.Path('C:\\Users\\tarasov-a\\Desktop').resolve() / file_name # путь из текущей папки + имя файла
    doc = fitz.open(path)  # открыть файл
    text = ''

    for page in doc:  # извлечь текст постранично
        text += page.get_text()

    if text == '':  # если текст не удалось считать
        print('PDF text is not extracted. Change the fitz module to read the file.')
        Execution()

    ans = text
    return ans


def define_find_words():  # задать ключевые слова для поиска
    words_find = set()
    while True:
        word = str(input('Type the key word to look for. Push the Enter key to leave. '))
        if word == '': # условие выхода - пустая строка
            print('You finished entering the words. ')
            print(*words_find)
            break
        else:
            words_find.add(word)

    search_words = list(dict.fromkeys(words_find))
    ans = search_words
    return ans


def get_list_svn():  # получить список файлов из директории svn
    pysvn.Client.set_default_username('tarasov-a')  # логин для входа
    pysvn.Client.set_default_password('FXYfC6dh')  # пароль для входа
    result_find_words = []
    path = str(input('Type the path to the directory in svn. '))
    while True:  # проверка, является ли строкой
        if not pysvn.Client.is_url(path):
            print('The path is invalid. Try another one. ')
            path = str(input('The path is '))
        else:
            break

    index = path.rfind('svn/')
    if index != -1:
        path = pathlib.Path('https://svn.protei.ru/svn/' + path[index + 4:])
        entry_list = pysvn.Client.ls(path)
        for entry in entry_list:
            result_find_words.append(entry.name)


def main_pdf():
    if os.name == 'Windows':
        print('Prepare for pain!')
    # переход в директорию с pdf
    pdf_dir = input('Type the path to the directory with the pamr/pdra pdf. ')
    path_pdf = full_path(pdf_dir)
    os.chdir(path_pdf)
    # открытие файла pdf и извлечение текста целиком
    pdf_name = input('Type the name of the pdf file with the pamr/pdra. ')
    path_pdf_name = full_path(pdf_name)
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
