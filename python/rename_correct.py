import pathlib
import warnings

def text_correction(path_file):
    indeces = [5, 6, 7, 8, 9, 10, 12, 13, 14]
    path = pathlib.Path(path_file).resolve()

    if len(pathlib.Path(path).name) < 15: 
        warnings.warn('It\'s too short!')
    else:
        list_text = list(pathlib.Path(path).name)
        
        if not str(list_text[4]) == '.':
            list_text.insert(4, '.')

        if not str(list_text[11]) == '.':
            list_text.insert(11, '.')

        for index in indeces:
            if str(list_text[index]) == 'З':
                list_text[index] = str('3')

            if str(list_text[index]) == 'О':
                list_text[index] = str('0')

    if len(list_text) > 16:
        if str(list_text[-1:-3]) == str('СЬБ'):
            del list_text[-2]

        if str(list_text[-1:-2]) == str('СЬ'):
            list_text[-1] = str('Б')

    # converse the list to the string
    ans = ''.join(list_text)
    print(ans)
    return ans
