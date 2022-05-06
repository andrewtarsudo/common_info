from typing import Optional, Union, Any
import datetime
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter
from decimal import Decimal
from _style_work_item import _StyleWorkItem, _StyleWorkItemList


class ExcelProp:
    """
    Define the Excel Worksheet properties.

    Constants:
        dict_headers --- mapping states and indexes;\n
        dict_headers_short --- mapping issue states and indexes;\n

    Class params:
        dict_pyxl_row --- the dictionary of the PyXLRow instances;\n
        dict_pyxl_work_item --- the dictionary of the PyXLWorkItem instances;\n

    Properties:
        ws --- the worksheet;\n
        name --- the instance name;\n
        bottom_right --- the bottom-right cell;\n
        max_column --- the max column index;\n
        max_column_letter --- the max column letter;\n
        max_row --- the max row value;\n
        cell_from_coord --- the cell from its coord;\n
        headers --- the header cells;\n
        headers_row --- the header rows;\n
        list_state_row --- get the non-empty rows in the table;\n
        tasks --- get the PyXLRow instances;\n

    Functions:
        cell_in_range(start_coord, end_coord) --- generate the cell from range;\n
        check_empty(item) --- get the cell emptiness flag;\n
        list_state_item(state) --- get the non-empty rows with issues of the state;\n
        get_work_items(row) --- get the PyXLWorkItem instances in the row;\n
        get_column_date(date) --- get the column letter for the specified date;\n
    """
    dict_headers = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3, 'Легенда': 4}
    dict_headers_short = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3}

    dict_pyxl_row = dict()
    dict_pyxl_work_item = dict()

    def __init__(self, ws: Worksheet, name: str, styles: _StyleWorkItemList):
        self.ws = ws
        self.name = name
        self.styles = styles

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

    def get_column_date(self, date: datetime.date) -> str:
        """
        Get the column letter for the specified date.

        :param datetime.date date: the date
        :return: the column_letter.
        :rtype: str
        """
        cell: Cell
        for cell in self.cell_in_range("G1", "NR1"):
            if convert_datetime_date(cell.value) == date:
                return cell.column_letter

    @property
    def bottom_right(self) -> Cell:
        """
        Get the bottom-right cell.

        :return: the bottom-right cell.
        :rtype: Cell
        """
        max_row = self.ws.max_row
        max_col = self.ws.max_column
        return self.ws.cell(max_row, max_col)

    @property
    def max_column(self) -> int:
        """
        Get the max column value.

        :return: the column index.
        :rtype: int
        """
        return self.bottom_right.column

    @property
    def max_column_letter(self) -> str:
        """
        Get the max column letter.

        :return: the column letter.
        :rtype: str
        """
        return self.bottom_right.column_letter

    @property
    def max_row(self) -> int:
        """
        Get the max row value.

        :return: the row number.
        :rtype: int
        """
        return self.bottom_right.row

    def cell_in_range(self, start_coord: str, end_coord: str):
        """
        Convert the cell range to the cell generator in the range.

        :param str start_coord: the start cell coordinate
        :param str end_coord: the end cell coordinate
        :return: the generator of cells.
        """
        if check_coord(coord=start_coord) and check_coord(coord=end_coord):
            min_row, max_row, min_col, max_col = range_coord(start_coord=start_coord, end_coord=end_coord)
            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    coord = f'{get_column_letter(col)}{row}'
                    yield self.ws[coord]

    @property
    def headers(self) -> list[Cell]:
        """
        Get the header cells.

        :return: the cells.
        :rtype: list[Cell]
        """
        end_coord = f"B{self.bottom_right.row}"
        return [cell for cell in self.cell_in_range("B3", end_coord) if cell.value in ExcelProp.dict_headers]

    @property
    def headers_row(self) -> list[int]:
        """
        Get the header row values.

        :return: the list of header rows.
        :rtype: list[int]
        """
        return [header.row for header in self.headers]

    def check_empty(self, item: Union[int, str, Cell]) -> bool:
        """
        Check if the cell is empty.

        :param item: the cell value
        :type item: int or str or Cell
        :return: the emptiness flag.
        :rtype: bool
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
        """
        Get the non-empty rows with issues of the state.

        :param str state: the state
        :return: the non-empty rows with the state.
        :rtype: list[int]
        """
        index = self.dict_headers_short[state]
        return [row for row in range(self.headers_row[index], self.headers_row[index + 1]) if not self.check_empty(row)]

    @property
    def list_state_row(self) -> list[list[int]]:
        """
        Get the non-empty rows with issues for all states.

        :return: the non-empty rows.
        :rtype: list[list[int]]
        """
        return [self.list_state_item(state) for state, index in self.dict_headers_short.items()]

    @property
    def tasks(self):
        """
        Set the PyXLRow instances from the table.

        :return: the PyXLRow instances.
        :rtype: list[PyXLRow]
        """
        return [PyXLRow(self, self.ws[f"C{row}"]) for list_state in self.list_state_row for row in list_state]

    def pyxl_row_names(self) -> list[str]:
        """
        Get the PyXLRow issue names.

        :return: the issue names.
        :rtype: list[str]
        """
        return [task.issue_name for task in self.tasks]

    def get_work_items(self, row: int) -> list[tuple[datetime.date, Union[int, Decimal], str, str]]:
        """
        Get the work items.

        :param int row: the table row
        :return: the work items.
        :rtype: list[tuple[date, Union[int, Decimal], str, str]]
        """
        work_items: list[tuple[datetime.date, Union[int, Decimal], str, str]] = []
        work_item_row: tuple[Cell]
        cell: Cell
        for cell in self.cell_in_range(start_coord=f"G{row}", end_coord=f"NR{row}"):
            # get the cell column
            column = cell.column_letter
            if cell.value is None:
                continue
            else:
                # get style
                if cell.has_style:
                    cell_style: str = cell.style.name
                else:
                    cell_style = "basic"
                work_items.append(
                    (self.ws[f'{column}1'].value, cell.value, cell.coordinate, cell_style))
        return work_items

    def get_merged(self):
        """
        Specify the _PyXLMerged instances.

        :return: the _PyXLMerged instances.
        :rtype: list[_PyXLMerged]
        """
        list_rows = [value for item in self.list_state_row for value in item]
        return [_PyXLMerged(self, self.ws[f"C{row}"]) for row in list_rows]


def check_coord(coord: str) -> bool:
    """
    Verify the cell coordinate.

    :param str coord: the cell coordinates
    :return: the verification flag.
    :rtype: bool
    """
    flag = False
    try:
        coordinate_to_tuple(coord)
    except TypeError as e:
        print(f'TypeError {str(e)}. Incorrect value type.\n')
        print(f'coordinate = {coord}')
    except ValueError as e:
        print(f'ValueError {str(e)}. Incorrect value.\n')
        print(f'coordinate = {coord}')
    except OSError as e:
        print(f'OSError {e.errno}, {e.strerror}.\n')
        print(f'coordinate = {coord}')
    else:
        flag = True
    finally:
        return flag


def range_coord(start_coord: str, end_coord: str):
    """
    Convert the range string with the start and end coordinates to the tuple:\n
    (min_row, min_col, max_row, max_col)\n

    :param start_coord: the start cell coordinate, str
    :param end_coord: the end cell coordinate, str
    :return: the values for iteration of the tuple[int, int, int, int] type.
    """
    # convert start coordinate
    start_row, start_column = coordinate_to_tuple(start_coord)
    # convert end coordinate
    end_row, end_column = coordinate_to_tuple(end_coord)
    # find min and max values
    min_row = min(start_row, end_row)
    max_row = max(start_row, end_row)

    min_col = min(start_column, end_column)
    max_col = max(start_column, end_column)
    return min_row, max_row, min_col, max_col


def convert_spent_time(spent_time: Any) -> Decimal:
    """Converts the spent time to the specified format."""
    return Decimal(spent_time).normalize()


def convert_datetime_date(value: Any) -> Optional[datetime.date]:
    """
    Converts the datetime or None to the date.\n
    :param value: the value to convert, Any
    :return: the converted value or None of the date type.
    """
    if isinstance(value, datetime.date):
        return value
    elif isinstance(value, datetime.datetime):
        return value.date()
    else:
        return None


class PyXLRow:
    """
    Define the issue parameters from the table.

    Class params:
        attrs --- the attributes:\n
        "issue", "state", "summary", "parent", "deadline";\n
        index --- the unique instance identifier, 0-based;\n

    Params:
        excel_prop_name --- the ExcelProp name, str;\n
        issue --- the issue cell, Cell;\n

    Properties:
        excel_prop --- the ExcelProp instance;\n
        ws --- the Worksheet instance;\n
        coord --- the cell coordinate;\n
        row --- the table row;\n
        state --- the issue state;\n
        parent --- the parent issue name, B column;\n
        issue_name --- the issue name, C column;\n
        summary --- the issue summary, D column;\n
        deadline --- the issue deadline, E column;\n
        commentary --- the issue commentary, NS column;\n

    Functions:
        to_tuple() --- convert to the tuple;\n
    """
    attrs = ("issue_name", "state", "summary", "parent", "deadline")

    __slots__ = ("excel_prop", "issue")

    def __init__(self, excel_prop: ExcelProp, issue: Cell):
        self.excel_prop = excel_prop
        self.issue = issue

        self.excel_prop.dict_pyxl_row[self.issue_name] = self

    def __str__(self):
        return f"PyXLRow: excel_prop = {self.excel_prop}, cell = {self.issue.coordinate}"

    def __repr__(self):
        return f"PyXLRow(excel_prop={self.excel_prop}, issue={self.issue.coordinate})"

    def __hash__(self):
        return hash((self.excel_prop.name, self.issue.coordinate))

    def __key(self):
        return self.excel_prop.name, self.issue.coordinate

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

    @property
    def ws(self) -> Worksheet:
        """
        Get the Worksheet instance.

        :return: the Worksheet instance.
        :rtype: Worksheet
        """
        return self.excel_prop.ws

    @property
    def coord(self) -> str:
        """
        Get the cell coordinate.

        :return: the cell coordinate.
        :rtype: str
        """
        return self.issue.coordinate

    @property
    def row(self) -> int:
        """
        Get the cell row.

        :return: the cell row.
        :rtype: int
        """
        return self.issue.row

    @property
    def parent(self) -> Optional[str]:
        """
        Get the parent issue name.

        :return: the parent issue name.
        :rtype: str or None
        """
        return self.ws[f"B{self.row}"].value

    @property
    def issue_name(self) -> str:
        """
        Get the issue name.

        :return: the issue name.
        :rtype: str
        """
        return self.issue.value

    @property
    def summary(self) -> str:
        """
        Get the issue summary.

        :return: the issue summary.
        :rtype: str
        """
        return self.ws[f"D{self.row}"].value

    @property
    def deadline(self) -> Optional[datetime.date]:
        """
        Get the issue deadline.

        :return: the issue deadline.
        :rtype: date or None
        """
        return convert_datetime_date(self.ws[f"E{self.row}"].value)

    @property
    def commentary(self) -> Optional[str]:
        """
        Get the issue commentary.

        :return: the issue commentary.
        :rtype: str or None
        """
        return self.ws[f"NS{self.row}"].value

    def state(self) -> str:
        """
        Get the issue state.

        :return: the issue state.
        :rtype: str 
        """
        for state in ExcelProp.dict_headers_short.keys():
            if self.row in self.excel_prop.list_state_item(state):
                return state
            else:
                continue

    def to_tuple(self):
        """
        Represent the instance as a tuple.

        :return: the tuple of the issue attributes.
        :rtype: tuple[str, str, str, str or None, datetime.date or None]
        """
        return tuple(getattr(self, attr) for attr in PyXLRow.attrs)


class PyXLWorkItem:
    """
    Define the work items in the table.

    Class params:
        cell_attrs --- the attributes of the class instances:\n
        number_format, alignment, border, fill, font, protection, data_type;\n
        attrs --- the attributes: "issue", "date", "spent_time";\n
        index --- the unique instance identifier, 0-based;\n

    Params:
        excel_prop_name --- the ExcelProp instance name;\n
        cell --- the cell in the table;\n
        style_name --- the cell style;\n

    Properties:
        excel_prop --- the ExcelProp instance;\n
        ws --- the Worksheet instance;\n
        coord --- the cell coordinate;\n
        row --- the cell row;\n
        spent_time --- the issue spent time;\n
        date --- the work item date;\n
        cell_style_params --- the cell style parameters;\n

    Functions:
        set_style(style_name) --- set the cell style;
        _set_cell_attr(key, value) --- set the cell attributes;\n
        to_tuple() --- represent the instance as a tuple;\n
    """
    cell_attrs = ("number_format", "alignment", "border", "fill", "font", "protection", "data_type")
    attrs = ("issue", "date", "spent_time")

    __slots__ = ("excel_prop", "cell", "style_name")

    def __init__(self, excel_prop: ExcelProp, cell: Cell, style_name: str = "basic"):
        self.excel_prop = excel_prop
        self.cell = cell
        self.style_name = style_name

        self.excel_prop.dict_pyxl_work_item[self.issue] = self

    def __str__(self):
        return f"excel_prop_name = {self.excel_prop.name}, cell = {self.cell}"

    def __repr__(self):
        return f"PyXLWorkItem(excel_prop_name={self.excel_prop.name}, cell={self.cell})"

    def __hash__(self):
        return hash((self.excel_prop.name, self.cell.coordinate))

    def __key(self):
        return self.excel_prop.name, self.cell.row, self.cell.column_letter

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
    def ws(self) -> Worksheet:
        """
        Get the Worksheet instance.

        :return: the Worksheet instance.
        :rtype: Worksheet
        """
        return self.excel_prop.ws

    @property
    def row(self) -> int:
        """
        Get the cell row.

        :return: the cell row.
        :rtype: int
        """
        return self.cell.row

    @property
    def spent_time(self) -> Decimal:
        """
        Get the work item spent time.

        :return: the spent time.
        :rtype: int or Decimal
        """
        return convert_spent_time(self.cell.value)

    @property
    def date(self) -> datetime.date:
        """
        Get the work item date.

        :return: the work item date.
        :rtype: date
        """
        column: str = self.cell.column_letter
        return convert_datetime_date(self.ws[f"{column}1"].value)

    @property
    def cell_style(self) -> _StyleWorkItem:
        """
        Get the cell style.

        :return: the cell style.
        :rtype: _StyleWorkItem
        """
        return self.excel_prop.styles[self.style_name]

    @property
    def issue(self):
        return self.ws[f"C{self.row}"].value

    def set_style(self, style_name: str):
        """
        Set the cell style.

        :param style_name: the style name, str
        :return: None.
        """
        self.excel_prop.styles.set_style(style_name, self.cell.coordinate)

    @property
    def cell_style_params(self):
        """
        Get the cell attributes.\n
        {number_format, Alignment, Border, PatternFill, Font, Protection}

        :return: the cell parameters.
        :rtype: tuple
        """
        return tuple(getattr(self.cell, attr) for attr in PyXLWorkItem.cell_attrs)

    def _set_cell_attr(self, key: str, value):
        """
        Set the cell attributes.\n
        {number_format, Alignment, Border, PatternFill, Font, Protection}

        :param str key: the cell attribute
        :param value: the attribute value
        :return: None.
        """
        if key in PyXLWorkItem.cell_attrs:
            setattr(self.cell, key, value)
        else:
            print(f"AttributeError, {key} in not a valid attribute.")

    def to_tuple(self):
        """
        Represent the instance as a tuple.

        :return: the tuple of the issue work item attributes.
        :rtype: tuple[str, datetime.date, Decimal]
        """
        return tuple(getattr(self, attr) for attr in PyXLWorkItem.attrs)


class _PyXLMerged:
    """
    Get the PyXLRow and PyXLWorkItem instances in the row.

    Params:
        excel_prop_name --- the ExcelProp instance name;\n
        cell --- the base cell;\n

    Properties:
        excel_prop --- the ExcelProp instance;\n
        row --- the cell row;\n
        ws --- the Worksheet instance;\n
        pyxl_row --- the PyXLRow instance;\n
        work_items --- the PyXLWorkItem instances;\n

    Functions:
        get_item_attr(item, attr) --- get the work item attribute;\n
    """
    attrs = ("excel_prop", "cell")
    __slots__ = ("excel_prop", "cell")

    def __init__(self, excel_prop: ExcelProp, cell: Cell):
        self.excel_prop = excel_prop
        self.cell = cell

    @property
    def row(self) -> int:
        """
        Get the cell row.

        :return: the cell row.
        :rtype: int
        """
        return self.cell.row

    @property
    def ws(self) -> Worksheet:
        """
        Get the Worksheet instance.

        :return: the Worksheet instance.
        :rtype: Worksheet
        """
        return self.excel_prop.ws

    @property
    def pyxl_row(self) -> PyXLRow:
        """
        Get the PyXLRow instance.

        :return: the PyXLRow instance.
        :rtype: PyXLRow
        """
        pyxl_row: PyXLRow
        for pyxl_row in self.excel_prop.dict_pyxl_row.values():
            if self.cell == pyxl_row.issue:
                return pyxl_row

    @property
    def work_items(self) -> list[PyXLWorkItem]:
        """
        Get the PyXLWorkItem instances.

        :return: the PyXLWorkItem instances.
        :rtype: list[PyXLWorkItem]
        """
        return [work_item for work_item in self.excel_prop.dict_pyxl_work_item.values() if work_item.row == self.row]

    def __hash__(self):
        return hash(self.cell.coordinate)

    def __iter__(self):
        return (self.getitem_id(work_item) for work_item in self.work_items)

    def __eq__(self, other):
        if isinstance(other, _PyXLMerged):
            return self.cell.coordinate == other.cell.coordinate
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _PyXLMerged):
            return self.cell.coordinate != other.cell.coordinate
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, _PyXLMerged):
            return self.row < other.row
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, _PyXLMerged):
            return self.row > other.row
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, _PyXLMerged):
            return self.row <= other.row
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, _PyXLMerged):
            return self.row >= other.row
        else:
            return NotImplemented

    def __getattribute__(self, key: str):
        if key in _PyXLMerged.attrs:
            return object.__getattribute__(self, key)
        else:
            print(f"AttributeError, {key} in not a valid attribute.")
            return None

    def __setattr__(self, key: str, value):
        if key in self.__slots__:
            object.__setattr__(self, key, value)
        else:
            print(f"AttributeError, {key} in not a valid attribute.")

    def __getitem__(self, item):
        if item in self.work_items:
            return self.work_items[item]
        else:
            print(f"KeyError, {item} in not a valid key.")
            return None

    def __setitem__(self, key, value):
        self.work_items[key] = value

    def __contains__(self, item):
        if isinstance(item, PyXLRow):
            return self.pyxl_row == item
        elif isinstance(item, PyXLWorkItem):
            return item in self.work_items
        else:
            return NotImplemented

    def get_item_attr(self, item: int, attr: str):
        """
        Get the work item attribute.

        :param int item: the work item index
        :param str attr: the work item attribute name
        :return: the attribute value.
        """
        list_attr = ("date", "spent_time", "coord", "style")
        if attr not in list_attr:
            print(f"AttributeError, the attribute {attr} is not specified.")
            return None
        elif item not in self.work_items:
            print(f"KeyError, {item} is not a proper list item index.")
            return None
        else:
            return getattr(self.__getitem__(item), attr)

    @property
    def issue_name(self):
        return self.pyxl_row.issue_name


def main():
    pass


if __name__ == "__main__":
    main()
