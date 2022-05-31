import re
from typing import Optional
from collections import namedtuple
from pprint import pprint


dict_type: dict[tuple, int] = {
    ("Name", "Description", "Type", "O/M", "Version", "Logic"): 0,
    ("Name", "Description", "Type", "Default", "O/M", "Version"): 1,
    ("Name", "Description", "Type", "O/M", "Version"): 2,
    ("Name", "Description", "Type", "Default", "O/M", "Version", "Logic"): 3,
}

dict_type_indexes = {
    0: {
        "Name": 0,
        "Description": 1,
        "Type": 2,
        "OM": 3,
        "Version": 4,
        "Logic": 5
    },
    1: {
        "Name": 0,
        "Description": 1,
        "Type": 2,
        "Default": 3,
        "OM": 4,
        "Version": 5
    },
    2: {
        "Name": 0,
        "Description": 1,
        "Type": 2,
        "OM": 3,
        "Version": 4
    },
    3: {
        "Name": 0,
        "Description": 1,
        "Type": 2,
        "Default": 3,
        "OM": 4,
        "Version": 5,
        "Logic": 6
    }
}

Params = namedtuple("Params", ("Name", "OM", "Description"))


def parse_line(line: str):
    pattern_empty_cell = re.compile(r"\|\s*\|")
    if not line.startswith("|"):
        line_vert_separator = " ".join(("|", line, "|"))
    else:
        line_vert_separator = line
    line_upd = re.sub(pattern_empty_cell, "| None |", line_vert_separator)
    sub_lines = line_upd.strip().split("|")
    res = [sub_line.strip() for sub_line in sub_lines[1:-1]]
    return [sub_line.strip() for sub_line in sub_lines[1:-1]]


# def type_correction(line: str) -> str:
#     print(line)
#     # type_info = parse_line(line)[2]
#     pattern = re.compile(r"\[(.*)]\(#.*\)")
#     pattern_sub = re.compile(r"\[(.*)]")
#     if re.findall(pattern_sub, type_info):
#         sub_string = re.findall(pattern_sub, type_info)[0]
#         return re.sub(pattern, sub_string, type_info)
#     else:
#         return type_info


def type_sentence(line: str) -> str:
    type_info = parse_line(line)[2]
    # type_corrected = type_correction(type_info)
    # return "".join(("Тип — ", type_corrected, "."))
    return type_info


class TableMarkdown:
    def __init__(self, text_table: list[str] = None):
        if text_table is None:
            text_table: list[str] = []
        self.text_table = text_table
        if len(text_table) > 2:
            del self.text_table[1]
        self.dict_lines: dict[int, Params] = dict()

    @property
    def num_columns(self) -> int:
        return len(self.col_names)

    @property
    def col_names(self) -> list[str]:
        return parse_line(self.text_table[0])

    def __len__(self):
        return len(self.text_table)

    @property
    def table_type(self) -> int:
        for key, value in dict_type.items():
            if key == tuple(self.col_names):
                return dict_type[key]
            else:
                continue
        print("None type is found.")
        return -1

    @property
    def type_indexes(self) -> Optional[dict[str, int]]:
        try:
            indexes = dict_type_indexes[self.table_type]
        except KeyError as e:
            print(f"KeyError, {str(e)}.")
            return None
        else:
            return indexes

    def add_none(self, line_parsed: list[str]):
        diff = self.num_columns - len(line_parsed)
        if diff > 0:
            additional = diff * ["None"]
            return line_parsed.extend(additional)
        else:
            return line_parsed

    def parsed_line(self, line: str):
        if self.type_indexes is None:
            raise KeyError("KeyError. Table type: -1")
        lines = parse_line(line)
        lines_full = self.add_none(lines)
        index_om = self.type_indexes["OM"]
        return Params(lines_full[0], lines_full[index_om], self.combine_description(line))

    @property
    def description_index(self) -> int:
        return self.type_indexes["Description"]

    @property
    def default_index(self) -> Optional[int]:
        if "Default" in self.type_indexes.keys():
            return self.type_indexes["Default"]
        else:
            return None

    def default_sentence(self, line: str) -> Optional[str]:
        if self.default_index is None:
            return None
        else:
            default_info = parse_line(line)[self.default_index]
            if default_info in ("None", "\-"):
                return None
            return "".join(("Значение по умолчанию — ", default_info, "."))

    @property
    def version_index(self) -> Optional[int]:
        if "Version" in self.type_indexes.keys():
            return self.type_indexes["Version"]
        else:
            return None

    def version_sentence(self, line: str):
        if self.version_index is None:
            return None
        else:
            version_info = parse_line(line)[self.version_index]
            if version_info == "None":
                return None
            return "".join(("Актуально для версий ", version_info, "."))

    @property
    def logic_index(self) -> Optional[int]:
        if "Logic" in self.type_indexes.keys():
            return self.type_indexes["Logic"]
        else:
            return None

    def logic_sentence(self, line: str):
        if self.logic_index is None:
            return None
        else:
            logic_info = parse_line(line)[self.logic_index]
            if logic_info == "None":
                return None
            return "".join(("Используется для ", logic_info, "."))

    def note_sentence(self, line: str):
        note_lines: list[str] = ["Примечание."]
        if self.default_index is not None and self.default_sentence(line) is not None:
            note_lines.append(self.default_sentence(line))
        if self.version_index is not None and self.version_sentence(line) is not None:
            note_lines.append(self.default_sentence(line))
        if len(note_lines) == 1:
            return None
        else:
            return " ".join(note_lines)

    def combine_description(self, line: str):
        complete_description_lines = []
        lines = parse_line(line)
        # add the description
        complete_description_lines.append(lines[self.description_index])
        # add the parameter type
        complete_description_lines.append(f"\n{type_sentence(line)}")
        # add the default value if exists
        if self.default_index is not None and self.default_sentence(line) is not None:
            complete_description_lines.append(self.default_sentence(line))
        if self.version_index is not None and self.version_sentence(line) is not None:
            complete_description_lines.append(self.default_sentence(line))
        if self.note_sentence(line) is not None:
            complete_description_lines.append(f"\n{self.note_sentence(line)}")
        return " ".join(complete_description_lines)

    def parse_table(self):
        for index, line in enumerate(self.text_table[1:]):
            parsed_line = self.parsed_line(line)
            self.dict_lines[index] = parsed_line

    @property
    def param_values(self) -> list[str]:
        return [item.Name for item in self.dict_lines.values()]

    @property
    def om_values(self) -> list[str]:
        return [item.OM for item in self.dict_lines.values()]

    @property
    def description_values(self) -> list[str]:
        return [item.Description for item in self.dict_lines.values()]


def main():
    sentinel = ""
    text_table = [line for line in iter(input, sentinel)]
    md_table = TableMarkdown(text_table)
    print(len(md_table))
    # for line in md_table.text_table:
    #     print(line)
    md_table.parse_table()
    # print(md_table.description_index)
    # print(md_table.default_index)
    # print(md_table.version_index)
    # print(md_table.logic_index)
    print(md_table.param_values)
    print(md_table.om_values)
    print(md_table.description_values)



if __name__ == "__main__":
    main()
