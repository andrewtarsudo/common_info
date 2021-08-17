import fitz
import os

def find_text (filename, substring, length):
    doc = fitz.open(filename)
    pamr_pdra = []
    for page in doc:
        text = page.get_text("text")
        index = -1

        while True:
            index = text.find(str(substring), index + 1)
            if index == -1
                print("There is no such substring")
                break
            pamr_pdra.append(text[index:index + length])

        print("All values are found!")
    print("Close the file!")
    print(pamr_pdra)
    fitz.close(filename)


def rename (path, old_name, new_name):
    input_path = input("Путь до каталога с файлами")
    path = os.path.normpath(os.path.abspath(input_path))
    if os.path.exists(path):
        os.chdir(path)
        try:
            os.rename(old_name, new_name)
            print("Success! Now the filename is " + new_name)
        except FileExistsError:
            print("Error!")

    else:
        print("Check the table of names, something went wrong")
