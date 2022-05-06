from collections import Counter


def main():
    list_values = iter(line for line in input(""))
    list_values_upd = [line.strip() for line in list_values]
    cnt = Counter(list_values_upd)
    non_unique = [line for line, cnt_repeats in cnt.items() if cnt_repeats > 1]
    print(non_unique)
