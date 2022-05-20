"""
Generate the randomized string of specified length and types of chars allowed.

The possible modes:
    lower Latin chars;\n
    upper Latin chars;\n
    digits;\n
    special chars;\n

The modes can be combined any way. Lower Latin chars are considered as basic and included by default.
The length should be lower than the number of allowed chars. Nonetheless, otherwise, the random string is generated
though it should be an error.
"""

import random
import numpy

DEFAULT_LEN = 8
YES_COMMANDS = ("y", "yes", "+", "1", "true")
NO_COMMANDS = ("n", "no", "-", "0", "false")

LOWER_LATIN_CHARS = "abcdefghijklmnopqrstuvwxyz"
UPPER_LATIN_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGIT_CHARS = "0123456789"
SPEC_CHARS = "!@#$%^&*()_+=-<>/{}[]"


def get_full_chars(is_upper: bool, is_digit: bool, is_spec: bool) -> str:
    """
    Specify the allowed chars.

    :param bool is_upper: flag to use the upper Latin chars;
    :param bool is_digit: flag to use the digits;
    :param bool is_spec: flag to use the special chars;
    :return: the full list of allowed chars.
    :rtype: str
    """
    include: list = []
    include.append(LOWER_LATIN_CHARS)
    if is_upper:
        include.append(UPPER_LATIN_CHARS)
    if is_digit:
        include.append(DIGIT_CHARS)
    if is_spec:
        include.append(SPEC_CHARS)
    return "".join(include)


def verify_length(user_input_length: str):
    """
    Verify that the user input is proper and not equal to zero.

    :param str user_input_length: the user length of the random string
    :return: the modified proper length value or default: DEFAULT_LEN
    :rtype: int
    """
    try:
        # convert to integer
        len_generate_random = int(user_input_length)
        # validate if the value is non-zero
        numpy.divide(len_generate_random, len_generate_random)
    except ValueError as e:
        print(f"ValueError {e.args}. The default value of {DEFAULT_LEN} chars is set.")
        return DEFAULT_LEN
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError {e.args}. The default value of {DEFAULT_LEN} chars is set.")
        return DEFAULT_LEN
    except OSError as e:
        print(f"OSError {e.errno}, {e.strerror}. The default value of {DEFAULT_LEN} chars is set.")
        return DEFAULT_LEN
    else:
        # convert the negative integer
        if len_generate_random < 0:
            print("The absolute value is used.")
            return numpy.abs(len_generate_random)
        else:
            return len_generate_random


def verify_enough_chars(length: int, chars: str) -> tuple[int, str]:
    """
    Verify that the number of chars is long enough.

    :param int length: the required length
    :param chars: the allowed chars
    :return: the required length and the multiplied chars if necessary.
    :rtype: tuple[int, str]
    """
    multiplier = numpy.floor_divide(length, len(chars)) + 1
    return length, chars * multiplier


def get_random(length: int, allowed_chars: str) -> str:
    """
    Get the random string of the specified length.

    :param int length: the length of the string
    :param str allowed_chars: the allowed chars
    :return: the random string from the defined chars.
    :rtype: str
    """
    chars_generated = random.choices(allowed_chars, k=length)
    random.shuffle(chars_generated)
    return "".join(chars_generated)


def bool_user_input(user_input: str, default: bool) -> bool:
    """
    Convert the user input to the bool type for the flags.

    If the input is not Yes or No defined, the default value is implemented.

    :param str user_input: the user input
    :param bool default: the default value
    :return: the converted input or default.
    :rtype: bool
    """
    if user_input.lower() in YES_COMMANDS:
        return True
    elif user_input.lower() in NO_COMMANDS:
        return False
    else:
        return default


def main():
    len_input = input(f"Type the length of the generated string. Default: {DEFAULT_LEN}\n")
    # display the prompts to set the values
    print(f"To answer Yes, type any value of {YES_COMMANDS}.")
    print(f"To answer No, type any value of {NO_COMMANDS}.")
    print(f"Otherwise, the default value is implemented.\n")
    # specify the mode
    upper = input("Include the upper Latin chars? Default: yes\n")
    digit = input("Include the digits? Default: yes\n")
    spec = input("Include the special chars? Default: no\n")
    # process the length
    len_generated_string = verify_length(len_input)
    # process the mode
    is_upper = bool_user_input(upper, True)
    is_digit = bool_user_input(digit, True)
    is_spec = bool_user_input(spec, False)

    allowed_chars = get_full_chars(is_upper, is_digit, is_spec)
    len_generated_string, allowed_chars = verify_enough_chars(len_generated_string, allowed_chars)
    print(get_random(len_generated_string, allowed_chars))
    input("Push any button to terminate the program ...")


if __name__ == "__main__":
    main()
