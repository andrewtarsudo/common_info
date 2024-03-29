from terms import Const, Term, TermList
from markdown import MarkdownFile


class User:
    def __init__(self, md_file: MarkdownFile = None, term_list: TermList = None):
        self.md_file = md_file
        self.term_list = term_list

    def __terms(self) -> list[Term]:
        return self.term_list.terms

    def terms_to_md(self) -> list[str]:
        return [format(term, "md") for term in self.__terms()]

    def add_term(self, short: str, full: str, rus: str = None, commentary: str = None):
        new_term = Term(short, full, rus, commentary)
        self.__terms().append(new_term)


def main():
    md_file = MarkdownFile()
    term_list = TermList()
    user = User(md_file, term_list)
    pass


if __name__ == "__main__":
    main()
