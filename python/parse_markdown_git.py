import re
from typing import Optional

dict_type: dict[set[str], int] = {
    {"Name", "Description", "Type", "O/M", "Version", "Logic"}: 0,
    {"Name", "Description", "Type", "Default", "O/M", "Version"}: 1,
    {"Name", "Description", "Type", "O/M", "Version"}: 2
}

dict_type_indexes = {
    0: {
        "Name": 0,
        "Description": 1,
        "Type": 2,
        "O/M": 3,
        "Version": 4,
        "Logic": 5
    },
    1: {
        "Name": 0,
        "Description": 1,
        "Type": 2,
        "Default": 3,
        "O/M": 4,
        "Version": 5
    },
    2: {
        "Name": 0,
        "Description": 1,
        "Type": 2,
        "O/M": 3,
        "Version": 4
    }
}

dict_line = {
    "Name": ["Name"],
    "O/M": ["O/M"],
    "Description": ["Description", "Type", "Default"]
}


def parse_line(line: str):
    pattern_empty_cell = re.compile(r"\|\s*\|")

    line_upd = re.sub(pattern_empty_cell, "| None |", line)

    if not line.startswith("|"):
        sub_lines = line.strip().split("|")
        return [replace_none(sub_line).strip() for sub_line in sub_lines]


def replace_none(line: str):
    if line == "None":
        return "---"


class TableMarkdown:
    def __init__(self, text_table: list[str] = None):
        if text_table is None:
            text_table = []
        self.text_table = text_table
        self.output_table = ""

    @property
    def num_columns(self):
        return len(self.col_names)

    @property
    def col_names(self):
        return parse_line(self.text_table[0])

    @property
    def table_type(self) -> int:
        for key, value in dict_type.items():
            if key == set(self.col_names):
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

    def parsed_line(self, line: str):
        if self.type_indexes is None:
            raise KeyError("KeyError. Table type: -1")
        lines = parse_line(line)
        dict_params: dict[str, list[str]] = {
            "Name": [], "O/M": [], "Description": []
        }
        dict_params["Name"].append(lines[0])
        index_om = self.type_indexes["O/M"]
        dict_params["O/M"].append(lines[index_om])

    @property
    def description_index(self):
        return self.type_indexes["Description"]

    @property
    def type_index(self):
        return self.type_indexes["Type"]

    def type_correction(self, line: str):
        type_info = parse_line(line)[self.type_index]
        pattern = re.compile(r"\[(.*)]\(#.*\)")
        pattern_sub = re.compile(r"\[(.*)]")
        if re.findall(pattern_sub, type_info):
            sub_string = re.findall(pattern_sub, type_info)[0]
            return re.sub(pattern, sub_string, type_info)
        else:
            return type_info

    def type_sentence(self, line: str):
        type_info = parse_line(line)[self.type_index]
        type_correction = self.type_correction(type_info)
        return " — ".join(("Тип", type_correction))

    @property
    def default_index(self):
        if "Default" in self.type_indexes.keys():
            return self.type_indexes["Default"]
        else:
            return None

    def default_sentence(self, line: str):
        if self.default_index is None:
            return None
        else:
            type_info = parse_line(line)[self.default_index]
            return " — ".join(("Значение по умолчанию", type_info))

    def combine_description(self, line: str):
        description_lines = []
        lines = parse_line(line)
        description_lines.append(lines[self.description_index])


def main():
    pass


if __name__ == "__main__":
    main()
