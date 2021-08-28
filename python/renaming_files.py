import fitz
import os
import pathlib

path_original = ""
path_destination = ""
length_num = 18

def change_directory(path_dir):
    path = pathlib.PureWindowsPath(path_dir)
    while True:
        if pathlib.exists(path) and pathlib.is_dir(path):
            path_new = pathlib.resolve(path)
            os.chdir(path_new)
            break
        elif str(path) == "stop":
            print("You stopped work.")
            path_new = Exception()
            break
        else:
            print("Path is incorrect.")
            path_redef = str(input("Type the path to the directory"))
            path_dir = pathlib.PureWindowsPath(path_redef)
    
    ans = str(path_new)
    return ans

def change_name(path_orig, path_dest, filename, new_name):
    pathorig = pathlib.PureWindowsPath(path_orig)
    pathdest = pathlib.PureWindowsPath(path_dest)
    file_old = pathlib.resolve(pathorig) / str(filename) + '.pdf'
    file_new = pathlib.resolve(pathdest) / str(new_name) + '.pdf'
    replaced_file = pathlib.Path(file_old).replace(file_new)
    ans = str(pathlib.name(replaced_file))
    return ans

def find_text(filename, *argv):
    path = pathlib.WindowsPath(pathlib.Path.cwd() / str(filename) + '.pdf')
    doc = fitz.open(path)
    text = ''
    search_number = []
    for page in doc:
        text += page.getText()
        start = 0
        i = 0
        for arg in argv:
            while True:
                if text.find(str(arg), start) == -1:
                    print("There are no substrings left")
                    break
                else:
                    index = text.find(str(arg), start)
                    search_number[i] = text[index:index + length_num]
                    i += 1
                    start = index + length_num
    for unit in search_number:
        ans = print(str(unit))
    return search_number

