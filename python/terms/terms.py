from bisect import bisect_left
import logging
from copy import copy
from pathlib import Path
from typing import Optional, Union
from collections import Counter


class Const:
    """
    Define the constants.

    Params:
        dict_short_id --- the dictionary of the Term identifiers and Term short.
    """
    dict_short_id: dict[int, str] = dict()


def binary_search(values: list[str], search_value: str, min_index: int = 0, max_index: int = None) -> int:
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
    sorted_values = sorted(values)
    position = bisect_left(sorted_values, search_value, min_index, max_index)
    print("The position is associated with the sorted sequence.")
    return position if position != max_index and sorted_values[position] == search_value else -1


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


def add_term(short: str, full: str, meaning_rus: str = None):
    return Term(short, full, meaning_rus)


class TermList:
    """
    
    """
    def __init__(self, terms: list[Term] = None):
        if terms is None:
            terms = []
        self.terms = terms
        self.dict_short_id = dict()

    def _identifiers(self) -> list[int]:
        return [term.identifier for term in self.terms]

    def _shorts(self) -> list[str]:
        return [term.short for term in self.terms]

    def _rus(self) -> list[str]:
        return [term.rus for term in self.terms]

    def binary_by_short(self, short: str) -> Optional[Term]:
        position = binary_search(self._shorts(), short)
        if position != -1:
            return self.terms[position]
        else:
            logging.warning(f"The term {short} is not in the dictionary.")
            return None

    def __short_same_keys(self):
        cntr = Counter(self.dict_short_id.values())
        counter = +cntr
        return [item for item in counter.keys() if counter[item] > 1]

    def __short_same_values(self, item: str):
        list_identifiers = []
        list_shorts = copy(self._shorts())
        return [identifier for identifier in self.dict_short_id if self.dict_short_id[identifier] == item]

    def dict_short_id_same(self):
        dict_same = dict()
        for item in self.__short_same_keys():
            dict_same[item] = self.__short_same_values(item)
        return dict_same

    def search_short(self, short: str):
        if short in self.dict_short_id_same():
            return self.dict_short_id_same()[short]
        else:
            return self.binary_by_short(short)

    def write_to_file(self, path: Union[Path, str]):
        try:
            if isinstance(path, str) and not path.endswith(".md"):
                raise ValueError
            if isinstance(path, Path) and path.suffix != ".md":
                raise ValueError
            path_file = Path(path).resolve()
            if not path_file.exists():
                path_file.touch()
            with open(path_file, "w") as file:
                file.writelines([format(term, "md") for term in self.terms])
        except ValueError as e:
            print(f"{e.__class__.__name__} {e.args}")
        except PermissionError as e:
            print(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
        except IsADirectoryError as e:
            print(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
        except RuntimeError as e:
            print(f"{e.__class__.__name__} {e.args}")
        except OSError as e:
            print(f"{e.__class__.__name__} {e.errno}, {e.strerror}")
        else:
            print("The file is ready.")

    def _sorted_terms(self):
        return sorted(self.terms)
    
    def get_terms(self, parsed_md: list[tuple[str, str, str, str]]):
        for short, full, rus, commentary in parsed_md:
            self.terms.append(Term(short, full, rus, commentary))
        return self._sorted_terms()
            

def main():
    # filename = "./basic_log.log"
    # fmt = "%(levelName)s %(asctime)s, %(funcName) --- %(message)s"
    # level = logging.INFO
    # logging.basicConfig(filename=filename, format=fmt, level=level)
    list_values = ["a", "b", "c", "a", "a", "c"]
    cntr = Counter(list_values)
    counter = +cntr
    values = [item for item in counter.keys() if counter[item] > 1]
    print(values)


if __name__ == "__main__":
    main()
