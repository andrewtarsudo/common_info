import re
import requests


class MarkdownFile:
    """
    Specify the Markdown operation instance.

    Params:
        url --- the URL to the Markdown file;\n

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

    def text(self) -> list[str]:
        """
        Specify the text from the GitHub repo file.

        :return: the file contents.
        :rtype: list[str]
        """
        response = requests.get(self.url)
        return response.text.split("\n")


def main():
    pass


if __name__ == "__main__":
    main()
