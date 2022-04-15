import re
from pprint import pprint
from typing import Optional
import keyboard
import pyperclip

str_input: str = "qwertyuiop[]asdfghjkl;'\\zxcvbnm,./`1234567890-=|~!@#$%^&*()_+{}:\"|<>?"
str_output: str = "йцукенгшщзхъфывапролджэ\\ячсмитьбю.ё1234567890-=/Ё!\"№;%:?*()_+ХЪЖЭ/БЮ,"

dict_io: dict[str, str] = dict(zip(list(str_input), list(str_output)))

common_chars = [item for item in dict_io if dict_io[item] == item]

error_pattern = re.compile(r".*\s\*!\s.*")


class _KeyboardSettings:
    # keyboard_event = keyboard.KeyboardEvent()
    wait_hotkey = "ctrl+shift+/"

    # keyboard.add_hotkey(wait_hotkey, print("Hi"))
    # keyboard.wait()



def user_input():

    pass


def convert_text_char(text: str) -> tuple[str, bool]:
    new_chars: list = list()
    error: bool = False

    for char in list(text):
        if char not in dict_io:
            new_chars.append(" *! ")
            error = True
        else:
            new_chars.append(dict_io[char])
    return "".join(new_chars), error


def convert():
    for text_i in iter(input()):
        if re.match(error_pattern, text_i) is not None:
            output_line, error = convert_text_char
            if error:
                print("Incorrect input!")
                return
        else:
            strings, errors = [convert_text_char(line) for line in text_i.split(" !* ")]
            if not any(item is True for item in errors):
                output_line = " !* ".join(strings)
            else:
                print("Incorrect input!")
                return

        print(output_line)


def main():
    # print(keyboard.get_hotkey_name(["left ctrl", "shift", "?"]))
    # print(keyboard.key_to_scan_codes(wait_hotkey))
    # print(keyboard.read_hotkey())
    # print(keyboard.stash_state())
    wait_hotkey = "ctrl+shift+/"
    keyboard.read_hotkey()
    hk = keyboard.add_hotkey("a", print("Hi"))
    # print(keyboard._canonical_names.canonical_names)
    # keyboard.wait(hk)


if __name__ == "__main__":
    main()
