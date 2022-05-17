import sqlite3
from bisect import bisect_left
import logging
from typing import Optional
from collections import Counter


class Const:
    dict_short_id: dict[int, str] = dict()


def binary_search(values: list[str], search_value: str, min_index: int = 0, max_index: int = None):
    if max_index is None:
        max_index = len(values)
    position = bisect_left(values, search_value, min_index, max_index)
    return position if position != max_index and values[position] == search_value else -1


class Term:
    index = 0

    def __init__(self, short: str, full: str, meaning_rus: str = None):
        self.short = short
        self.full = full
        self.meaning_rus = meaning_rus
        self.identifier = Term.index

        Term.index += 1
        Const.dict_short_id[self.identifier] = self.short

    def __format__(self, format_spec):
        return f"{self.short}\t{self.full}, {self.meaning_rus}"

    def __repr__(self):
        return f"Term({self.short}, {self.full}, {self.meaning_rus})"

    def __str__(self):
        return f"short: {self.short}, full: {self.full}, rus: {self.meaning_rus}"

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
    def __init__(self, name: str, terms: list[Term] = None):
        if terms is None:
            terms = []
        self.name = name
        self.terms = terms
        self.dict_short_id = dict()

    def _identifiers(self) -> list[int]:
        return [term.identifier for term in self.terms]

    def _shorts(self) -> list[str]:
        return [term.short for term in self.terms]

    def _rus(self) -> list[str]:
        return [term.meaning_rus for term in self.terms]

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


def main():
    # filename = "terms_log.log"
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
