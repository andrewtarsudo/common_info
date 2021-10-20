import ocrmypdf
import os
import sys
import pathlib

def foo():
    path_input_file = 'C:\\Users\\tarasov-a\\Desktop\\Other_docs\\doc00042620200625141242.pdf'
    input_file_ocr = pathlib.Path(path_input_file).resolve()
    print(input_file_ocr)
    path_output_file = 'C:\\Users\\tarasov-a\\Desktop\\Other_docs\\test.pdf'
    output_file_ocr = pathlib.Path(path_output_file).resolve()
    print(output_file_ocr)
    languages_ocr = 'rus'
    # print(ocrmypdf.ocr())
    print(os.path.isfile(output_file_ocr))
    ocrmypdf.ocr(input_file_ocr, output_file_ocr, language=languages_ocr)
    print(os.path.isfile(output_file_ocr))
    

if __name__ == '__main__':  # To ensure correct behavior on Windows and macOS
    ocrmypdf.ocr(input_file, output_file, language='rus')


foo()

    
