import sys
from bisect import bisect_left
import logging
import requests
import re
from pathlib import Path
from typing import Optional, Union
from collections import Counter


def binary_search(
        values: Union[list[str], list[int]],
        search_value: Union[str, int],
        min_index: int = 0,
        max_index: int = None) -> int:
    """
    Specify the binary search to accelerate the common one.

    :param values: the list to search the value
    :type values: list[str]
    :param str search_value: the value to search
    :param int min_index: the lower bound, default = 0
    :param max_index: the higher bound, default = len(values)
    :return: the searched value position in the list if the value is in the list.
    :rtype: int
    """
    if max_index is None:
        max_index = len(values)
    # sort the values
    sorted_values = sorted(values)
    position = bisect_left(sorted_values, search_value, min_index, max_index)
    # print the note
    print("The position is associated with the sorted sequence.")
    return position if position != max_index and sorted_values[position] == search_value else -1


def process_user_input(prompt: str) -> Optional[str]:
    """
    Update the user input processing.

    :param str prompt: the input prompt
    :return: the processed input.
    :rtype: str or None
    """
    user_input = input(prompt)
    if user_input in Const.terminate_cmd:
        print("The program is terminating ...")
        sys.exit()
    else:
        return process_user_input(user_input)


def parse_list_values(input_terms: str) -> list[str]:
    """
    Convert the multiple value string to the sequence.

    :param str input_terms: the input line
    :return: the parsed items.
    :rtype: list[str]
    """
    return input_terms.strip().split()


class Const:
    """
    Define the constants.

    Params:
        dict_short_id --- the dictionary of the Term identifiers and Term short;\n
        start_cmd --- the commands to start the program;\n
        terminate_cmd --- the commands to terminate the program;\n
        program_prompt --- the short instruction to operate with the program;\n
    """
    dict_short_id = dict()
    start_cmd = ("__start__", "__launch__")
    terminate_cmd = ("___exit__", "__quit__", "__stop__")

    program_prompt = """
        The commands:
        __start__, __launch__ --- start the program;\n
        "__term__" --- search the terms;\n
        "__add__" --- add the term;\n
        "__write__" --- write the term list to the *.md file;\n
        "___exit__", "__quit__", "__stop__" --- terminate the program;\n\n
        The __add__ command is executed with the __write__ one since the direct changes may corrupt the GitHub 
        repo file and make it unavailable.\n\n
        Separate the term to search with spaces. The table has no values having two parts.\n\n
        Most actions are logged to the file 'terms.log' in the folder where the program is launched.
        """


class MarkdownFile:
    """
    Specify the Markdown operation instance.

    Params:
        url --- the URL to the Markdown file;\n

    Properties:
        name --- the Markdown file name;\n

    Functions:
        _split_columns(line) --- split the line by the columns;\n
        _split_first_rus_char(line) --- split the line by the first non-Latin character;\n
        _split_dash(line) --- split the line by the minus sign, en dash, and em dash;\n
        parse_md_line(line) --- parse the Markdown line to the short, full, rus, comment parameters;\n
        parse_md_file(line) --- parse the Markdown text;\n
        text() --- the text from the GitHub repo file;\n
    """
    def __init__(self, url: str = "https://raw.githubusercontent.com/andrewtarsudo/common_info/master/annex/Terms.md"):
        self.url = url

    def __str__(self):
        return f"Markdown file name: {self.name}, GitHub repo: andrewtarsudo/common_info/"

    def __repr__(self):
        return f"MarkdownFile({self.url})"

    @property
    def name(self):
        """
        Get the GitHub repo file name.

        :return: the file name.
        :rtype: str
        """
        return self.url.split("/")[-1]

    @staticmethod
    def _split_columns(line: str) -> list[str]:
        """
        Split the line by the columns.

        :param str line: the text string
        :return: the column strings.
        :rtype: list[str]
        """
        edit_line = line.strip("|").strip()
        return edit_line.split(" | ")

    @staticmethod
    def _split_first_rus_char(line: str) -> tuple[str, str]:
        """
        Split the line by the first non-Latin character.

        :param str line: the text string
        :return: the resulted strings.
        :rtype: tuple[str, str]
        """
        split_index = -1
        # verify if the char is an ASCII one
        for index, char in enumerate(line):
            if not char.isascii():
                split_index = index
                break
            else:
                continue
        # verify if the line contains the non-Latin characters
        if split_index != -1:
            return line[:split_index - 2], line[split_index:]
        else:
            return line, ""

    @staticmethod
    def _split_dash(line: str) -> list[str]:
        """
        Split the line by the minus sign, en dash, and em dash.

        :param str line: the text string
        :return: the resulted strings.
        :rtype: list[str]
        """
        pattern = re.compile(' [-\u2013\u2014] ')
        return re.split(pattern, line)

    def parse_md_line(self, line: str) -> tuple[str, str, str, str]:
        """
        Parse the Markdown line to the short, full, rus, comment parameters.

        :param str line: the text string
        :return: the short, full, rus, comment parameters.
        :rtype: tuple[str, str, str, str]
        """
        short, upd_line = self._split_columns(line)
        full, rus_line = self._split_first_rus_char(upd_line)
        rus, comment = self._split_dash(rus_line)
        return short, full, rus, comment

    def parse_md_file(self) -> list[tuple[str, str, str, str]]:
        """
        Parse the Markdown text.

        :return: the parsed lines.
        :rtype: list[tuple[str, str, str, str]]
        """
        return [self.parse_md_line(line) for line in self.text()]

    def text(self) -> Optional[list[str]]:
        """
        Specify the text from the GitHub repo file.

        :return: the file contents.
        :rtype: list[str]
        """
        try:
            response = requests.get(self.url)
        except requests.HTTPError as e:
            logging.error(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
            raise requests.HTTPError("HTTPError, the connection error.")
        except OSError as e:
            logging.error(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
            raise OSError("OSError, the internal error.")
        else:
            return response.text.split("\n")


class Term:
    """
    Specify the term item.

    Class params:
        index --- the identifier;\n

    Params:
        identifier --- the instance identifier;\n
        short --- the short term;\n
        full --- the full term;\n
        rus --- the Russian equivalent;\n
        commentary --- the commentary to the term;\n
    """
    index = 0

    __slots__ = ("short", "full", "rus", "commentary", "identifier")

    def __init__(self, short: str, full: str, rus: str, commentary: str = None):
        self.short = short
        self.full = full
        self.rus = rus
        self.commentary = commentary
        self.identifier = Term.index

        Term.index += 1
        Const.dict_short_id[self.identifier] = self.short

    def __format__(self, format_spec: str = "all"):
        # the empty format
        if format_spec:
            return str(self)
        # the complete information
        elif format_spec == "all":
            format_commentary = f" ({self.commentary})" if not self.commentary else ""
            return f"{self.short}\t{self.full}, {self.rus}{format_commentary}"
        # the short term
        elif format_spec == "short":
            return f"Short: {self.short}"
        # the full term
        elif format_spec == "full":
            return f"Full term: {self.full}"
        # the Russian equivalent
        elif format_spec == "rus":
            return f"Russian equivalent: {self.rus}"
        # the Russian equivalent and commentary
        elif format_spec == "rus_commentary":
            format_commentary = f"\nAdditional information: {self.commentary}" if not self.commentary else ""
            return f"Russian equivalent: {self.rus}{format_commentary}"
        elif format_spec == "md":
            return f"| {self.short} | {self.full} | {self.rus} | {self.commentary} |"
        else:
            return repr(self)

    def __repr__(self):
        return f"Term({self.short}, {self.full}, {self.rus}, {self.commentary})"

    def __str__(self):
        return f"short: {self.short}, full: {self.full}, rus: {self.rus}, commentary: {self.commentary}"

    def __hash__(self):
        return hash((self.short, self.full))

    def __key(self):
        return self.short, self.full

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Term):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __lt__(self, other):
        if not isinstance(other, Term):
            return NotImplemented
        else:
            if self.short != other.short:
                return self.short < other.short
            else:
                return self.full < other.full

    def __gt__(self, other):
        if not isinstance(other, Term):
            return NotImplemented
        else:
            if self.short != other.short:
                return self.short > other.short
            else:
                return self.full > other.full

    def __le__(self, other):
        if not isinstance(other, Term):
            return NotImplemented
        else:
            return self.short <= other.short

    def __ge__(self, other):
        if not isinstance(other, Term):
            return NotImplemented
        else:
            return self.short >= other.short


class TermList:
    """
    Specify the list of terms.

    Params:
        terms --- the list of Term instances;\n
        dict_short_id --- the dictionary of the terms with the non-unique shorts;\n

    Properties:
        dict_short_id_same() --- specify the dictionary of the non-unique short terms;\n

    Functions:
        _identifiers() --- get the list of the term identifiers;\n
        _shorts() --- get the list of the term shorts;\n
        _rus() --- get the list of the Russian terms;\n
        binary_by_short(short) --- get the Term instance by the short with the binary search;\n
        binary_by_id(short) --- get the Term instance by the identifier with the binary search;\n
        search_short(short) --- get the Term instance by the short using the binary search;\n
        _sorted_terms() --- get the sorted Term items;\n
        generate_terms(parsed_md) --- get the sorted Term instances from the Markdown file;\n
    """
    def __init__(self, terms: list[Term] = None):
        if terms is None:
            terms = []
        self.terms = terms
        self.dict_short_id = dict()

    def __str__(self):
        return "The list of terms."

    def __repr__(self):
        return "TermList()"

    def _identifiers(self) -> list[int]:
        """
        Get the term identifiers.

        :return: the term identifiers.
        :rtype: list[str]
        """
        return [term.identifier for term in self.terms]

    def _shorts(self) -> list[str]:
        """
        Get the short terms.

        :return: the short terms.
        :rtype: list[str]
        """
        return [term.short for term in self.terms]

    def _rus(self) -> list[str]:
        """
        Get the Russian terms.

        :return: the Russian terms.
        :rtype: list[str]
        """
        return [term.rus for term in self.terms]

    def binary_by_short(self, short: str) -> Optional[Term]:
        """
        Get the Term instance by the short using the binary search.

        :param short: the short term
        :return: the Term instance if exists.
        :rtype: Term or None
        """
        position = binary_search(self._shorts(), short)
        # if the term exists
        if position != -1:
            return self.terms[position]
        # if the term does not exist
        else:
            logging.warning(f"WARNING: INCORRECT SHORT, {short}.")
            print(f"The short {short} is not in the dictionary.")
            return None

    def binary_by_id(self, identifier: int) -> Optional[Term]:
        """
        Get the Term instance by the identifier using the binary search.

        :param identifier: the term identifier
        :return: the Term instance if exists.
        :rtype: Term or None
        """
        position = binary_search(self._identifiers(), identifier)
        # if the term exists
        if position != -1:
            return self.terms[position]
        # if the term does not exist
        else:
            logging.warning(f"WARNING: INCORRECT ID, {identifier}.")
            print(f"The identifier {identifier} is not in the dictionary.")
            return None

    def __short_same_keys(self) -> list[str]:
        """Get the keys of the dictionary of the non-unique short terms."""
        cntr = Counter(self.dict_short_id.values())
        counter = +cntr
        return [item for item in counter.keys() if counter[item] > 1]

    def __short_same_values(self, item: str) -> list[int]:
        """Get the values of the dictionary of the non-unique short terms."""
        return [identifier for identifier in self.dict_short_id if self.dict_short_id[identifier] == item]

    @property
    def dict_short_id_same(self):
        """
        Specify the dictionary of the non-unique short terms.

        :return: the dictionary.
        :rtype: dict[str, list[int]]
        """
        dict_same: dict[str, list[int]] = dict()
        for item in self.__short_same_keys():
            dict_same[item] = self.__short_same_values(item)
        return dict_same

    def search_short(self, short: str) -> Union[Term, list[Term], None]:
        """
        Get the Term instance by the short using the binary search.

        :param short: the short term
        :return: the Term instance.
        :rtype: Term or list[Term] or None
        """
        if short in self.dict_short_id_same:
            return [self.terms[identifier] for identifier in self.dict_short_id_same[short]]
        else:
            return self.binary_by_short(short)

    def _sorted_terms(self) -> list[Term]:
        """
        Sort the Term items.

        :return: the sorted list of terms.
        :rtype: list[Term]
        """
        return sorted(self.terms)

    def generate_terms(self, parsed_md: list[tuple[str, str, str, str]]) -> list[Term]:
        """
        Get the sorted Term instances from the Markdown file.

        :param parsed_md: the parsed lines of the file
        :type parsed_md: list[tuple[str, str, str, str]]
        :return: the sorted terms.
        :rtype: list[Term]
        """
        for short, full, rus, commentary in parsed_md:
            self.terms.append(Term(short, full, rus, commentary))
        return self._sorted_terms()


class User:
    """
    Specify the user instance.

    Params:
        md_file --- the Markdown file;\n
        term_list --- the TermList instance;\n

    Functions:
        __terms() --- get the terms;\n
        terms_to_md() --- convert the terms to the Markdown format;\n
        exec_command(cmd) --- execute the command, default __term__;\n
        show_terms() --- search the terms;\n
        add_term() --- add the term to the list;\n
        write_to_file() --- write the terms to the file;\n
    """
    def __init__(self, md_file: MarkdownFile = None, term_list: TermList = None):
        self.md_file = md_file
        self.term_list = term_list

    def __str__(self):
        return f"Markdown file: {self.md_file.name}"

    def __repr__(self):
        return f"User({self.md_file}, {self.term_list})"

    def __terms(self) -> list[Term]:
        """
        Get the Term instances.

        :return: the list of terms.
        :rtype: list[Term]
        """
        return self.term_list.terms

    def terms_to_md(self) -> list[str]:
        """
        Convert the terms to the Markdown format.

        :return: the list of lines.
        :rtype: list[str]
        """
        return [format(term, "md") for term in self.__terms()]

    def exec_command(self, cmd: str = "__term__"):
        """
        Execute the user input command.

        :param str cmd: the command to execute
        :return: None.
        """
        command = process_user_input(cmd)
        if command == "__term__":
            self.show_terms()
        elif command == "__add__":
            self.add_term()
        elif command == "__write__":
            self.write_to_file()
        elif command in Const.start_cmd:
            return None
        else:
            logging.error(f"ERROR: INCORRECT COMMAND, {command}")
            print("Incorrect command.")
            return None

    def show_terms(self) -> list[str]:
        """
        Show the terms attributes.

        :return: the term parameters list.
        :rtype: list[str]
        """
        format_type: Optional[str] = process_user_input("Set the format type to output:\n")
        search: list[str] = parse_list_values(process_user_input("Set the short terms:\n"))
        # process the search items from the input
        search_result = []
        for short_item in search:
            search_result.append(self.term_list.search_short(short_item))
        logging.debug(f"Format type: {format_type}, Search: {search_result}")
        # output the terms in the defined format
        return [format(search_item, format_type) for search_item in (*search_result,)]

    def add_term(self):
        """Add the new Term instance."""
        short = process_user_input("Set the short term:\n")
        full = process_user_input("Set the full term:\n")
        rus = process_user_input("Set the Russian term:\n")
        commentary = process_user_input("Set the commentary to the term:\n")
        # create new term
        new_term = Term(short, full, rus, commentary)
        logging.debug(f"Short: {short}, Full: {full}, Rus: {rus}, Commentary: {commentary}")
        # add to the term list
        self.__terms().append(new_term)
        self.write_to_file()

    def write_to_file(self):
        """Write the Term instances to the file."""
        path: str = process_user_input("Set the path to the *.md file:\n")
        # verify the file extension
        try:
            if isinstance(path, str) and not path.endswith(".md"):
                logging.error(f"ERROR: INCORRECT FILE TYPE, {path}")
                raise ValueError(f"The path '{path}' is not correct since the file is not *.md")
            path_file = Path(path).resolve()
            # create the file if it does not exist
            if not path_file.exists():
                path_file.touch()
            with open(path_file, "w") as file:
                file.writelines([format(term, "md") for term in self.__terms()])
        except ValueError as e:
            logging.error(f"{e.__class__.__name__} {e.args}")
        except PermissionError as e:
            logging.error(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
        except IsADirectoryError as e:
            logging.error(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
        except RuntimeError as e:
            logging.error(f"{e.__class__.__name__} {e.args}")
        except OSError as e:
            logging.error(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
        else:
            logging.debug(f"DEBUG: WRITTEN TO FILE, {path}")
            print("The file is ready.")


def main():
    # configure the log file
    filename = "./terms.log"
    fmt = "%(levelName)s %(asctime)s, %(funcName) --- %(message)s"
    level = logging.INFO
    encoding = "utf-8"
    logging.basicConfig(filename=filename, format=fmt, level=level, encoding=encoding)
    # set the basic instances
    md_file = MarkdownFile()
    term_list = TermList()
    user = User(md_file, term_list)
    # start the program
    user.exec_command("__start__")
    # output the prompt
    print(Const.program_prompt)

    while True:
        user.exec_command(process_user_input("Type the command:"))


if __name__ == "__main__":
    main()
