import sys

def Check(value):
    while True:
        try:
            int_value = int(value)
            if int_value <= 0:
                print ('Ehm, stop for a while.')
                value = input('Type the positive int.')
            else:
                break
        except ValueError:
            if (value == 'stop'):
                break
                main()
            else:
                print("What's wrong with you? Type the int positive value.")
                value = input('Try again.')

    return int_value

def main():
    while True:
        a = Check(input("Page number in each item: "))

        if (a % 4) != 0:
            print('Are you kidding?')
            a = Check(input('Page number in each item: '))

        b = Check(input('Number of items: '))
        c = Check(input('The first page to print: '))

        if c >= a:
            print('It exceeds the number of pages. WTF?')
            c = Check(input('The first page to print: '))
        else:
            break

    ans = []
    k = 0

    while k < b:
        ans.append(a * k + c)
        ans.append(a * k + c + 1)
        k += 1

    while k < 2 * b:
        ans.append(a * (2 * b - k) - c)
        ans.append(a * (2 * b - k) - c + 1)
        k += 1

    res = '{'

    for i in range (len(ans)):
        res = res + str(ans[i])
        res += ', '

    res = res[:-2] + '}'

    print(res)
    input()

main()
