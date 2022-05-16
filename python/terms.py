import sqlite3
import random
from bisect import bisect_left
import logging


logging.basicConfig(filename="terms.log")


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


class TermList:
    def __init__(self, name: str, terms: list[Term] = None):
        if terms is None:
            terms = []
        self.name = name
        self.terms = terms
        self.dict_short_id = dict()

    def _identifiers(self):
        return [term.identifier for term in self.terms]

    def _shorts(self):
        return [term.short for term in self.terms]

    def _rus(self):
        return [term.meaning_rus for term in self.terms]

    def binary_term_id(self, short: str):
        position = binary_search(self._shorts(), short)
        if position != -1:
            return self.terms[position]
        else:
            logging.warning(f"The term {short} is not in the dictionary.")
            return None
    
    
    
    
