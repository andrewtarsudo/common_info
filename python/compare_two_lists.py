# make a list from the multiple line input
def make_list():
    res_list = []
    while True:
        line = input()
        if not line == '':
            res_list.append(line)
        else:
            break
    return res_list


# sort the lists and check if each element of the first list is equal to the element of the second
def check_lists(list_1: list, list_2: list) -> bool:
    return list_1.sort() == list_2.sort()


# create two lists and compare them
def main():
    print('Type the first set of values. Finish the input with the empty line:')
    check_list_1 = make_list()
    print('Type the second set of values. Finish the input with the empty line:')
    check_list_2 = make_list()

    if check_lists(check_list_1, check_list_2):
        print('They are equal')
    else:
        print('They are different')


if __name__ == '__main__':
    main()
