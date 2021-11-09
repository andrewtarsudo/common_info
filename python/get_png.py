import get_contents
import pathlib
import fitz


def get_png(path_file):
    path = pathlib.Path(path_file).resolve()
    doc = fitz.open(path)  # open document

    for page in doc:  # iterate through the pages
        pix = page.get_pixmap()  # render page to an image
        path_new = str(path.parent)+'\\'+ str(path.stem)+'_page_%i.png' %page.number
        print(path_new)
        pix.save(path_new)  # store image as a PNG


def main():
    path_dir = input('Path to the directory: ')
    path = pathlib.Path(path_dir).resolve()

    dir_contents = get_contents.get_content_dir(path)

    for item in dir_contents:
        get_png(item)


if __name__ == '__main__':
    main()
