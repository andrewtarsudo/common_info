from copy import copy
from typing import Optional, Union, Any
import datetime
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from const import Const
from openpyxl.utils.cell import coordinate_to_tuple, coordinate_from_string, get_column_letter
from decimal import Decimal
from _style_work_item import _StyleWorkItem, _StyleWorkItemList
from openpyxl.styles.cell_style import CellStyle

dict_excel_prop = dict()
dict_pyxl_row = dict()
dict_pyxl_work_item = dict()


def reverse_dict(dict_init: dict):
    dict_reverse = dict()
    for key, value in dict_init.items():
        dict_reverse[value] = key
    return dict_reverse


class ExcelProp:
    dict_headers = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3, 'Легенда': 4}
    dict_headers_short = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3}

    def __init__(self, ws: Worksheet, name: str):
        self.ws = ws
        self.name = name

        dict_excel_prop[self.name] = self

    def __str__(self):
        return f"Worksheet is {self.ws}, name is {self.name}"

    def __repr__(self):
        return f"ExcelProp(ws={self.ws}, name={self.name})"

    def __hash__(self):
        return hash((self.ws, self.name))

    def __eq__(self, other):
        if isinstance(other, ExcelProp):
            return (self.ws == other.ws) and (self.name == other.name)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ExcelProp):
            return (self.ws != other.ws) and (self.name != other.name)
        else:
            return NotImplemented

    @property
    def bottom_right(self):
        max_row = self.ws.max_row
        max_col = self.ws.max_column
        return self.ws.cell(max_row, max_col)

    @property
    def max_column(self):
        return self.bottom_right.column

    @property
    def max_column_letter(self):
        return self.bottom_right.column_letter

    @property
    def max_row(self):
        return self.bottom_right.row

    def cell_from_coord(self, coord: str) -> Cell:
        return self.ws[f"{coord}"]

    def cell_in_range(self, start_coord: str, end_coord: str):
        yield self.ws[f"{Const.cell_in_range(start_coord, end_coord)}"]

    @property
    def headers(self) -> list[Cell]:
        end_coord = f"B{self.bottom_right.row}"
        return [cell for cell in self.cell_in_range("B3", end_coord) if cell.value in ExcelProp.dict_headers]

    @property
    def headers_row(self) -> list[int]:
        return [header.row for header in self.headers]

    @staticmethod
    def column_coord(coord: str) -> str:
        return coordinate_from_string(coord)[0]

    @staticmethod
    def row_coord(coord: str) -> int:
        return coordinate_from_string(coord)[1]

    def check_empty(self, item: Union[int, str, Cell]):
        """
        Checks if the cell is empty. The item may be:\n
        the cell, Cell;\n
        the cell coordinate, str;\n
        the row, int.\n
        :param item: the cell parameter, Union[int, str, Cell]
        :return: the flag if the cell is empty of the bool type.
        """
        if isinstance(item, Cell):
            return True if item.value is None else False
        elif isinstance(item, str):
            return True if self.ws[f"{item}"].value is None else False
        elif isinstance(item, int):
            if self.ws[f"B{item}"] | self.ws[f"C{item}"] | self.ws[f"D{item}"] | self.ws[f"E{item}"] is not None:
                return False
            else:
                return True

    def list_state_item(self, state: str) -> list[int]:
        index = self.dict_headers_short[state]
        return [row for row in range(self.headers_row[index], self.headers_row[index + 1]) if not self.check_empty(row)]

    @property
    def list_state_row(self) -> list[list[int]]:
        return [self.list_state_item(state) for state, index in self.dict_headers_short.items()]

    def tasks(self):
        for list_state in self.list_state_row:
            for row in list_state:
                return PyXLRow.get_pyxl_row(self.name, f"C{row}")

    def get_work_items(self, row: int) -> list[tuple[datetime.date, Union[int, Decimal], str, str]]:
        work_items: list[tuple[datetime.date, Union[int, Decimal], str, str]] = []
        work_item_row: tuple[Cell]

        for coord in Const.cell_in_range(start_coord=f"G{row}", end_coord=f"NR{row}"):
            if self.ws[f"{coord}"].value is None:
                continue
            else:
                if self.ws[f"{coord}"].has_style:
                    cell_style: str = self.ws[f"{coord}"]._style.name
                else:
                    cell_style = "basic"
                work_items.append(
                    (self.ws[f'{Const.cell_column(coord)}1'].value, self.ws[f"{coord}"].value, coord, cell_style))

        return work_items

    def get_column_date(self, date: datetime.date):
        """
        
        :param date: 
        :return: 
        """
        for coord in Const.cell_in_range("G1", "NR1"):
            cell_value: Optional[datetime.date] = Const.convert_datetime_date(self.ws[f"{coord}"].value)
            if cell_value is not None and cell_value == date:
                return Const.cell_column(coord)


def convert_spent_time(spent_time: Any) -> Union[int, Decimal]:
    return spent_time if isinstance(spent_time, int) else Decimal(spent_time).normalize()


def str_to_excel_prop(name: str) -> Optional[ExcelProp]:
    return dict_excel_prop[name] if name in dict_excel_prop.keys() else None


def converter_work_items(
        work_items: list[tuple[Any, Any, str, str]]) -> list[tuple[datetime.date, Union[int, Decimal], str, str]]:
    work_items_final: list[tuple[datetime.date, Union[int, Decimal], str, str]] = []

    for work_item in work_items:
        date_init, spent_time_init, coord, style_name = work_item
        date_final: Optional[datetime.date] = Const.convert_datetime_date(date_init)
        spent_time_final = convert_spent_time(spent_time_init)
        work_items_final.append((date_final, spent_time_final, coord, style_name))

    return work_items_final


class PyXLRow:
    identifier = 0

    def __init__(self, excel_prop_name: str, issue: Cell):
        self.excel_prop_name = excel_prop_name
        self.issue = issue
        self.identifier = PyXLRow.identifier

        dict_pyxl_row[self.identifier] = self
        PyXLRow.identifier += 1

    def __str__(self):
        return f"PyXLRow: excel_prop_name = {self.excel_prop_name}, cell = {self.issue.coordinate}," \
               f"identifier = {self.identifier}"

    def __repr__(self):
        return f"PyXLRow(excel_prop_name={self.excel_prop_name}, issue={self.issue.coordinate})," \
               f"PyXLRow.identifier={self.identifier}"

    def __hash__(self):
        return hash((self.excel_prop_name, self.issue.coordinate))

    def __key(self):
        return self.excel_prop_name, self.issue.coordinate

    def __eq__(self, other):
        if isinstance(other, PyXLRow):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, PyXLRow):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, PyXLRow):
            return self.issue.row < other.issue.row
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PyXLRow):
            return self.issue.row > other.issue.row
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, PyXLRow):
            return self.issue.row <= other.issue.row
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PyXLRow):
            return self.issue.row >= other.issue.row
        else:
            return NotImplemented

    @classmethod
    def get_pyxl_row(cls, excel_prop_name: str, coord: str):
        excel_prop = dict_excel_prop[excel_prop_name]
        return cls(excel_prop_name, excel_prop.ws[f"{coord}"])

    @property
    def excel_prop(self):
        return dict_excel_prop[self.excel_prop_name]

    @property
    def ws(self):
        return self.excel_prop.ws

    @property
    def coord(self):
        return self.issue.coordinate

    @property
    def row(self):
        return self.issue.row

    @property
    def parent(self):
        return self.ws[f"B{self.row}"].value

    @property
    def issue_name(self):
        return self.ws[f"C{self.row}"].value

    @property
    def summary(self):
        return self.ws[f"D{self.row}"].value

    @property
    def deadline(self):
        return self.ws[f"E{self.row}"].value

    @property
    def commentary(self):
        return self.ws[f"NS{self.row}"].value

    def add_column(self, add_value: int):
        row, column = coordinate_to_tuple(self.coord)
        if add_value < 0 and column + add_value < 1:
            raise ValueError("Incorrect operand.")
        else:
            col_idx = column + add_value
            return self.ws[f"{get_column_letter(col_idx)}{row}"]


class PyXLWorkItem:
    identifier = 0
    attrs = ("number_format", "alignment", "border", "fill", "font", "protection", "data_type")

    def __init__(self, excel_prop_name: str, cell: Cell):
        self.excel_prop_name = excel_prop_name
        self.cell = cell
        self.identifier = PyXLWorkItem.identifier

        dict_pyxl_work_item[self.identifier] = self
        PyXLWorkItem.identifier += 1

    def __str__(self):
        return f"excel_prop_name = {self.excel_prop_name}, cell = {self.cell}, identifier = {self.identifier}"

    def __repr__(self):
        return f"PyXLWorkItem(excel_prop_name={self.excel_prop_name}, cell={self.cell}), identifier={self.identifier}"

    def __hash__(self):
        return hash((self.excel_prop_name, self.cell.coordinate))

    def __key(self):
        return self.excel_prop_name, self.cell.row, self.cell.column_letter

    def __eq__(self, other):
        if isinstance(other, PyXLWorkItem):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, PyXLWorkItem):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, PyXLWorkItem) and self.cell.row == other.cell.row:
            return self.cell.col_idx < other.cell.col_idx
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PyXLWorkItem) and self.cell.row == other.cell.row:
            return self.cell.col_idx > other.cell.col_idx
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, PyXLWorkItem) and self.cell.row == other.cell.row:
            return self.cell.col_idx <= other.cell.col_idx
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PyXLWorkItem) and self.cell.row == other.cell.row:
            return self.cell.col_idx >= other.cell.col_idx
        else:
            return NotImplemented

    @property
    def excel_prop(self) -> ExcelProp:
        return dict_excel_prop[self.excel_prop_name]

    @property
    def ws(self):
        return self.excel_prop.ws

    @property
    def coord(self):
        return self.cell.coordinate

    @property
    def spent_time(self):
        return self.cell.value

    @property
    def _get_cell_style(self):
        if self.cell.has_style:
            cell_style: CellStyle = self.cell.style
            if cell_style.name in _StyleWorkItemList.style_names:
                return cell_style.name
            else:
                _style_work_item = _StyleWorkItem.get_style_cell(cell_style.name, self.cell)
                return _style_work_item.name
        else:
            return None

    def set_style(self, style_name: str):
        if style_name not in _StyleWorkItemList.style_names:
            self.cell._style = copy(_StyleWorkItemList.basic())
        else:
            self.cell._style = copy(_StyleWorkItemList.get_style(style_name))

    @property
    def cell_style_params(self):
        return [self._get_cell_attr(attr) for attr in PyXLWorkItem.attrs]

    def _get_cell_attr(self, attr: str):
        if attr in PyXLWorkItem.attrs:
            return self.cell.__getattribute__(attr)
        else:
            return None

    def _set_cell_attr(self, attr: str, value):
        if attr in PyXLWorkItem.attrs:
            self.cell.__setattr__(attr, value)
        else:
            print(f"Attribute {attr} is not defined.")


def main():
    # path: pathlib.Path = pathlib.Path('/Users/user/Desktop/Отчет 2021 Тарасов.xlsx')
    # path: pathlib.Path = pathlib.Path(r'C:/Users/tarasov-a/Desktop/Отчет_2022_Тарасов.xlsx')
    # wb: Workbook = openpyxl.load_workbook(path)
    # print(wb._cell_styles)
    # print(wb._named_styles)
    # named_style: NamedStyle
    #
    # cell_style = named_style.as_tuple()
    # cell_style.numFmtId

    # copy_wb = wb._named_styles.sort()
    # wb._named_styles = []

    # wb._cell_styles = []
    # name_ws = wb.sheetnames[1]
    # ws = wb[name_ws]
    # excel_prop = ExcelProp(name='xlsx', ws=ws)
    # legend_row = excel_prop.headers[4]
    # print(legend_row)

    # list_cell_styles: CellStyleList = get_cell_styles(named_styles_list=list_named_styles)
    # wb.save('test_excel.xlsx')
    print('Everything is ok!')


if __name__ == "__main__":
    main()
