from copy import copy
from typing import Optional, Union, Any
import datetime
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter, column_index_from_string
from decimal import Decimal
from _style_work_item import _StyleWorkItem, _StyleWorkItemList


def convert_issue_state(state: str) -> str:
    """
    Converts the state to the table headers.

    :param str state: the issue state
    :return: the modified state.
    :rtype: str
    """
    # the issues to convert to the New/Paused
    to_new_paused = ('New', 'Paused', 'Canceled', 'Discuss')
    # the issues to convert to the Done/Test
    to_done_test = ('Done', 'Test', 'Review')
    # the issues to convert to the Verified
    to_verified = ('Closed',)

    if state in to_new_paused:
        modified_state = 'New/Paused'
    elif state in to_done_test:
        modified_state = 'Done/Test'
    elif state in to_verified:
        modified_state = 'Verified'
    else:
        print(f"Unspecified state {state} is found.")
        modified_state = state
    return modified_state


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
    """
    Convert the spent time to the specified format.

    :param spent_time: the converted value.
    :return: the decimal value.
    :rtype: Decimal
    """
    return Decimal(spent_time).normalize()


def convert_datetime_date(value: Any) -> Optional[datetime.date]:
    """
    Convert the datetime or None to the date.

    :param value: the value to convert
    :return: the date value.
    :rtype: datetime.date or None
    """
    if isinstance(value, datetime.date):
        return value
    elif isinstance(value, datetime.datetime):
        return value.date()
    else:
        return None


class ExcelProp:
    """
    Define the Excel Worksheet properties.

    Constants:
        dict_headers --- mapping states and indexes;\n
        dict_headers_short --- mapping issue states and indexes;\n
        dict_attr_column --- the dictionary of the issue attributes and columns;\n
        dict_state_style --- mapping states and styles;\n

    Class params:
        dict_pyxl_row --- the dictionary of the PyXLRow instances;\n
        dict_pyxl_work_item --- the dictionary of the PyXLWorkItem instances;\n
        dict_pyxl_merged --- the dictionary of the _PyXLMerged instances;\n

    Params:
        ws --- the worksheet;\n
        name --- the instance name;\n
        styles --- the _StyleWorkItemList instance;\n

    Properties:
        bottom_right --- the bottom-right cell to get the bounds;\n
        max_column --- the max column index;\n
        max_column_letter --- the max column letter;\n
        max_row --- the max row value;\n
        headers --- the header cells;\n
        headers_row --- the header row values;\n
        list_state_row --- the non-empty rows with issues for all states;\n
        get_pyxl_rows --- the PyXLRow instances from the table;\n

    Functions:
        get_column_date(date) --- get the column letter for the specified date;\n
        cell_in_range(start_coord, end_coord) --- convert the cell range to the cell generator;\n
        check_empty(item) --- verify if the cell is empty;\n
        list_state_item(state) --- get the non-empty rows with issues of the state;\n
        pyxl_row_names() --- get the PyXLRow issue names;\n
        num_pyxl_rows() --- get the issue numbers;\n
        get_work_items(row) --- get the work item instances in the row;\n
        get_merged() --- get the _PyXLMerged instances;\n
        delete_empty_rows_state(state) --- delete the empty rows for the state;\n
        delete_empty_rows() --- delete the empty rows in the workspace;\n
        get_merged_by_name(issue_name) --- get the _PyXLMerged instance by the issue name;
        get_row_by_name(issue_name) --- get the row by the issue name;
        add_work_item(issue_name, date, spent_time) --- add the work item;\n
    """
    dict_headers = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3, 'Легенда': 4}
    dict_headers_short = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3}
    dict_attr_column = {"parent": "B", "summary": "D", "deadline": "E", "commentary": "NT"}
    dict_state_style = {
        "New": "basic",
        "Active": "active",
        "Paused": "paused",
        "Done": "done",
        "Test": "test",
        "Verified": "verified_closed",
        "Closed": "verified_closed",
        "Discuss": "paused",
        "Review": "paused",
        "Canceled": "verified_closed"
    }

    dict_pyxl_row = dict()
    dict_pyxl_work_item = dict()
    dict_pyxl_merged = dict()
    dict_table_cell = dict()

    def __init__(self, ws: Worksheet, name: str, styles: _StyleWorkItemList):
        self.ws = ws
        self.name = name
        self.styles = styles

    def __str__(self):
        return f"Worksheet is {self.ws.title}, name is {self.name}"

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

    def get_column_by_date(self, date: datetime.date) -> str:
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
        Get the max column index.

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
        end_coord = f"B{self.max_row}"
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
        Verify if the cell is empty.

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
            cell_values = (
                self.ws[f"B{item}"].value, self.ws[f"C{item}"].value,
                self.ws[f"D{item}"].value, self.ws[f"E{item}"].value)
            if any(value is not None for value in cell_values):
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
        return [row for row in range(self.headers_row[index] + 1, self.headers_row[index + 1])
                if not self.check_empty(row)]

    def delete_empty_rows_state(self, state: str):
        """
        Delete empty rows for the state.

        :param str state: the state
        :return: None.
        """
        index = self.dict_headers_short[state]
        while any(self.check_empty(row) for row in range(self.headers_row[index] + 1, self.headers_row[index + 1] - 1)):
            for row in range(self.headers_row[index] + 1, self.headers_row[index + 1]):
                if self.check_empty(row):
                    self.ws.delete_rows(row)
                else:
                    continue
        return

    def delete_empty_rows(self):
        """Delete all empty rows in the workspace."""
        for state in self.dict_headers_short.keys():
            self.delete_empty_rows_state(state)

    @property
    def list_state_row(self) -> list[list[int]]:
        """
        Get the non-empty rows with issues for all states.

        :return: the non-empty rows.
        :rtype: list[list[int]]
        """
        return [self.list_state_item(state) for state in self.dict_headers_short.keys()]

    @property
    def get_pyxl_rows(self):
        """
        Get the PyXLRow instances from the table.

        :return: the PyXLRow instances.
        :rtype: list[PyXLRow]
        """
        return [PyXLRow(self, self.ws[f"C{row}"].value) for list_state in self.list_state_row for row in list_state]

    def pyxl_row_names(self) -> list[str]:
        """
        Get the PyXLRow issue names.

        :return: the issue names.
        :rtype: list[str]
        """
        return [pyxl_row.issue_name for pyxl_row in self.get_pyxl_rows]

    def num_pyxl_rows(self):
        """
        Get the issue number of different states.

        :return: the issue numbers.
        :rtype: list[int]
        """
        self.delete_empty_rows()
        return [len(item) for item in self.list_state_row]

    def get_work_items(self, row: int) -> list[tuple[datetime.date, Union[int, Decimal], str, str]]:
        """
        Get the work item instances in the row.

        :param int row: the table row
        :return: the work items.
        :rtype: list[tuple[date, int or Decimal, str, str]]
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
        Get the _PyXLMerged instances.

        :return: the _PyXLMerged instances.
        :rtype: list[_PyXLMerged]
        """
        list_rows = [value for item in self.list_state_row for value in item]
        return [_PyXLMerged(self, self.ws[f"C{row}"]) for row in list_rows]

    def add_row(self, state: str) -> int:
        """
        Get the row for the new issue in the table.

        :param str state: the issue state
        :return: the row number.
        :rtype: int
        """
        state_row = convert_issue_state(state)
        return max(self.list_state_item(state_row)) + 1

    def get_merged_by_name(self, issue_name: str):
        """
        Get the _PyXLMerged instance by the issue name.

        :param str issue_name: the issue name
        :return: the _PyXLMerged instance.
        :rtype: _PyXLMerged or None
        """
        if issue_name in self.pyxl_row_names():
            return self.dict_pyxl_merged[issue_name]
        return None

    def get_row_by_name(self, issue_name: str) -> Optional[int]:
        """
        Get the table row by the issue name.

        :param str issue_name: the issue name
        :return: the row number.
        :rtype: int or None
        """
        if issue_name in self.pyxl_row_names():
            return self.get_merged_by_name(issue_name).row
        return None

    def add_work_item(self, issue_name: str, date: datetime.date, spent_time: Union[int, Decimal]):
        """
        Add the work item to the table.

        :param str issue_name: the issue name
        :param date: the work item date
        :type date: datetime.date
        :param spent_time: the work item spent time
        :type spent_time: int or Decimal
        :return: None.
        """
        column = self.get_column_by_date(date)
        row = self.get_row_by_name(issue_name)
        cell: Cell = self.ws[f"{column}{row}"]
        cell.value = spent_time
        pyxl_work_item = PyXLWorkItem(self, cell)
        pyxl_work_item.set_style()

    def get_date_by_cell(self, cell: Cell) -> datetime.date:
        column = cell.column_letter
        raw_date = self.ws[f"{column}1"].value
        return convert_datetime_date(raw_date)

    def table_cells(self):
        return [TableCell(self, self.ws[f"C{row}"]) for list_state in self.list_state_row for row in list_state]

    def table_cell_names(self):
        return [table_cell.issue for table_cell in self.table_cells()]

    def get_table_cell(self, issue: str):
        if issue not in self.table_cell_names():
            print(f"ValueError, the issue {issue} not in the table.")
            return None
        else:
            for table_cell in self.table_cells():
                if table_cell.issue == issue:
                    return table_cell
                else:
                    continue

    def __non_unique(self):
        """
        Get the non-unique issue names.

        :return: the dictionary of the issue names and dates.
        :rtype: dict[str, list[TableCell]]
        """
        non_unique: dict[str, list[TableCell]] = dict()
        issue: str
        for issue, table_cell in self.dict.items():
            counter = Counter([work_item.date for work_item in work_items])
            non_unique_date = [key for key, value in counter.items() if value > 1]
            if not len(non_unique_date):
                non_unique[issue_name] = non_unique_date
        return non_unique

    def _join_work_items(self):
        """Join the non-unique work items."""
        for issue, dates in self.__non_unique.items():
            for date in dates:
                work_item: IssueWorkItem
                # cumulative sum
                cum_spent_time = numpy.cumsum(
                    [work_item.spent_time for work_item in self.dict_issue_work_item.values()
                     if work_item.issue == issue and work_item.date == date])
                # delete
                del_work_items = [
                    work_item for work_item in self.dict_issue_work_item.values()
                    if work_item.issue == issue and work_item.date == date]
                for item in del_work_items:
                    del item
                IssueWorkItem(self, issue, date, cum_spent_time)


class PyXLRow:
    """
    Define the issue parameters from the table.

    Class params:
        index --- the unique instance identifier, 0-based;\n
        attrs --- the attributes:\n
        "issue", "state", "summary", "parent", "deadline";\n

    Params:
        excel_prop_name --- the ExcelProp name;\n
        issue --- the issue cell;\n

    Properties:
        ws --- the Worksheet instance;\n
        coord --- the cell coordinate;\n
        row --- the table row;\n
        parent --- the parent issue name if exists;\n
        issue_name --- the issue name;\n
        summary --- the issue summary;\n
        deadline --- the issue deadline if exists;\n
        commentary --- the issue commentary;\n
        state --- the issue state;\n

    Functions:
        to_tuple() --- represent the instance as a tuple;\n
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
        Get the table row.

        :return: the table row.
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

    @property
    def state(self) -> str:
        """
        Get the issue state.

        :return: the issue state.
        :rtype: str
        """
        for state in self.excel_prop.dict_headers_short.keys():
            if self.row in self.excel_prop.list_state_item(state):
                return state
            else:
                continue

    def to_tuple(self):
        """
        Represent the instance as a tuple.

        :return: the tuple of the issue attributes.
        :rtype: tuple[str, str, str, str or None, date or None]
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
        ws --- the Worksheet instance;\n
        row --- the cell row;\n
        spent_time --- the work item spent time;\n
        date --- the work item date;\n
        cell_style --- the cell style;\n
        issue --- the issue name;\n
        cell_style_params --- the cell attributes;\n
        last_item --- last work item verification;\n

    Functions:
        set_style(style_name) --- set the cell style;\n
        _set_cell_attr(key, value) --- set the cell attributes;\n
        {number_format, Alignment, Border, PatternFill, Font, Protection}\n
        to_tuple() --- represent the instance as a tuple;\n
        __hyperlink_issue() --- get the PyXLRow issue hyperlink;\n
        __hyperlink_parent() --- get the PyXLRow parent issue hyperlink if exists;\n
        __parse_parent() --- specify the parent issue value in the table;\n
        __parse_issue() --- specify the issue value in the table;\n
        __parse_summary() --- specify the summary in the table;\n
        __parse_deadline() --- specify the deadline value in the table;\n
        __parse_formula() --- specify the formula to count the total time in the table;\n
        __parse_pyxl_row() --- specify the PyXLRow values in the table;\n
        __parse_work_item(work_item) --- specify the PyXLWorkItem value in the table;\n
        __parse_pyxl_items() --- specify the PyXLWorkItem values in the table;\n
        parse() --- specify all values in the table;\n
        _pyxl_row() --- get the associated _PyXLRow instance;\n
    """
    cell_attrs = ("number_format", "alignment", "border", "fill", "font", "protection", "data_type")
    attrs = ("issue", "date", "spent_time")

    __slots__ = ("excel_prop", "cell", "style_name")

    def __init__(self, excel_prop: ExcelProp, cell: Cell, style_name: str = "basic"):
        self.excel_prop = excel_prop
        self.cell = cell
        self.style_name = style_name

        self.excel_prop.dict_pyxl_work_item[self.issue].append(self)

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
        :rtype: Decimal
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
    def issue(self) -> str:
        """
        Get the issue name.

        :return: the issue name.
        :rtype: str
        """
        return self.ws[f"C{self.row}"].value

    def set_style(self, style_name: str = None):
        """
        Set the cell style.

        :param style_name: the style name, str
        :return: None.
        """
        if style_name is None:
            deadline = self._pyxl_row().deadline
            # if the date is a deadline
            if self.date == deadline:
                style_name = "deadline"
            else:
                # if the work item is not the last
                if not self.last_item:
                    style_name = "active"
                # otherwise, associate with the current state
                else:
                    style_name = self.excel_prop.dict_state_style[self._pyxl_row().state]
        self.style_name = style_name
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

    @property
    def last_item(self) -> bool:
        """
        Verify if the work item is the last one.

        :return: the verification flag.
        :rtype: bool
        """
        max_date = max(date for date, *_ in self.excel_prop.get_work_items(self.row))
        return self.date >= max_date

    def _pyxl_row(self):
        """
        Get the associated PyXLRow instance.

        :return: the PyXLRow instance.
        :rtype: PyXLRow
        """
        return self.excel_prop.dict_pyxl_row[self.issue]


class _PyXLMerged:
    """
    Get the PyXLRow and PyXLWorkItem instances in the row.

    Params:
        excel_prop_name --- the ExcelProp instance name;\n
        cell --- the base cell;\n

    Properties:
        row --- the table row;\n
        ws --- the Worksheet instance;\n
        pyxl_row --- the PyXLRow instance;\n
        work_items --- the PyXLWorkItem instances;\n
        issue_name --- the issue name;\n

    Functions:
        get_item_attr(item, attr) --- get the work item attribute;\n
        items_to_tuple() --- get the items in the tuple format;\n
        __hyperlink_issue() --- get the PyXLRow issue hyperlink;\n
        __hyperlink_parent() --- get the PyXLRow parent issue hyperlink if exists;\n
        __parse_parent(row) --- specify the parent issue value in the table;\n
        __parse_issue(row) --- specify the issue value in the table;\n
        __parse_summary(row) --- specify the summary in the table;\n
        __parse_deadline(row) --- specify the deadline value in the table;\n
        __parse_formula(row) --- specify the formula to count the total time in the table;\n
        __parse_pyxl_row(row) --- specify the PyXLRow values in the table;\n
        __parse_work_item(work_item, row) --- specify the PyXLWorkItem value in the table;\n
        __parse_pyxl_items(row) --- specify the PyXLWorkItem values in the table;\n
        parse(row) --- specify all values in the table;\n
        modify_pyxl_state(state) --- modify the issue state;\n
        work_item_style() --- set the work item styles;\n
    """

    __slots__ = ("excel_prop", "cell")

    def __init__(self, excel_prop: ExcelProp, cell: Cell):
        self.excel_prop = excel_prop
        self.cell = cell

        self.excel_prop.dict_pyxl_merged[self.issue_name] = self

    def __str__(self):
        return f"_PyXLMerged: {self.excel_prop.name}, cell: {self.cell.coordinate}"

    def __repr__(self):
        return f"_PyXLMerged({self.excel_prop}, {self.cell})"

    def __hash__(self):
        return hash(self.cell.coordinate)

    def __iter__(self):
        return (work_item for work_item in self.work_items)

    def __len__(self):
        return len(self.work_items)

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

    def __contains__(self, item):
        if isinstance(item, PyXLRow):
            return self.pyxl_row == item
        elif isinstance(item, PyXLWorkItem):
            return item in self.work_items
        else:
            return NotImplemented

    @property
    def row(self) -> int:
        """
        Get the table row.

        :return: the table row.
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
        else:
            return getattr(self.work_items[item], attr)

    @property
    def issue_name(self) -> str:
        """
        Get the issue name.

        :return: the issue name.
        :rtype: str
        """
        return self.pyxl_row.issue_name

    @property
    def last_work_item(self) -> str:
        """
        Get the last work item cell coordinates.

        :return: the cell coordinate.
        :rtype: str
        """
        max_date = max(work_item.date for work_item in self.work_items)
        for work_item in self.work_items:
            if work_item.date == max_date:
                return work_item.cell.coordinate
            else:
                continue

    def items_to_tuple(self) -> list[tuple[str, datetime.date, Decimal]]:
        """
        Get the items in the tuple format.

        :return: the converted items.
        :rtype: list[tuple[str, datetime.date, Decimal]]
        """
        return [work_item.to_tuple() for work_item in self.work_items]

    def __hyperlink_issue(self) -> str:
        """
        Get the PyXLRow issue hyperlink.

        :return: the link to the YouTrack issue.
        :rtype: str
        """
        return f"https://youtrack.protei.ru/issue/{self.issue_name}"

    def __hyperlink_parent(self) -> Optional[str]:
        """
        Get the PyXLRow parent issue hyperlink.

        :return: the link to the YouTrack issue.
        :rtype: str or None
        """
        return f"https://youtrack.protei.ru/issue/{self.pyxl_row.parent}" if not self.pyxl_row.parent else None

    def __parse_parent(self, row: int = None):
        """
        Specify the parent issue value in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        if not self.pyxl_row.parent:
            self.ws[f"B{row}"].value = self.pyxl_row.parent
            self.ws[f"B{row}"].data_type = "s"
            self.ws[f"B{row}"].hyperlink = self.__hyperlink_parent()

    def __parse_issue(self, row: int = None):
        """
        Specify the issue value in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        self.ws[f"C{row}"].value = self.issue_name
        self.ws[f"C{row}"].data_type = "s"
        self.ws[f"C{row}"].hyperlink = self.__hyperlink_issue()

    def __parse_summary(self, row: int = None):
        """
        Specify the summary in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        self.ws[f"D{row}"].value = self.pyxl_row.summary
        self.ws[f"D{row}"].data_type = "s"

    def __parse_deadline(self, row: int = None):
        """
        Specify the deadline value in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        if not self.pyxl_row.deadline:
            self.ws[f"E{row}"].value = self.pyxl_row.deadline
            self.ws[f"E{row}"].data_type = "d"

    def __parse_formula(self, row: int = None):
        """
        Specify the formula to count the total time in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        self.ws[f"NS{row}"].value = f"=SUM(G{row}:NR{row})"
        self.ws[f"NS{row}"].data_type = "f"

    def __parse_commentary(self, row: int = None):
        """
        Specify the commentary value in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        self.ws[f"NS{row}"].value = self.pyxl_row.commentary
        self.ws[f"NS{row}"].data_type = "s"

    def __parse_pyxl_row(self, row: int = None):
        """
        Specify the PyXLRow values in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        self.__parse_parent(row)
        self.__parse_issue(row)
        self.__parse_summary(row)
        self.__parse_deadline(row)
        self.__parse_formula(row)
        self.__parse_commentary(row)

    def __parse_work_item(self, work_item: PyXLWorkItem, row: int = None):
        """
        Specify the PyXLWorkItem value in the table.

        :param PyXLWorkItem work_item: the work item
        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        column = work_item.cell.column_letter
        style = work_item.style_name
        self.ws[f"{column}{row}"].value = work_item.spent_time
        self.ws[f"{column}{row}"].data_type = "n"
        self.ws[f"{column}{row}"].style = copy(self.excel_prop.styles[style])

    def __parse_pyxl_items(self, row: int = None):
        """
        Specify the PyXLWorkItem values in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        for work_item in self.work_items:
            self.__parse_work_item(work_item, row)

    def parse(self, row: int = None):
        """
        Specify all values in the table.

        :param int row: the row number
        :return: None.
        """
        if row is None:
            row = self.row
        self.__parse_pyxl_row(row)
        self.__parse_pyxl_items(row)

    def modify_pyxl_state(self, state: str):
        """
        Modify the issue state.

        :param state: the new state
        :return: None
        """
        # get the new row
        row: int = self.excel_prop.add_row(state)
        # add the row to the table
        self.ws.insert_rows(row)
        # get the old row
        old_row: int = self.row
        # parse the values to the new table row
        self.parse(row)
        # delete the old row
        self.ws.delete_rows(old_row)


class TableCell:
    def __init__(self, excel_prop: ExcelProp, cell: Cell):
        self.excel_prop = excel_prop
        self.cell = cell
        self.issue = str(cell.value)

        self.excel_prop.dict_table_cell[self.issue] = self

    def __str__(self):
        return f"Table cell: {self.cell.coordinate}"

    def __repr__(self):
        return f"TableCell({self.excel_prop}, {self.cell})"

    def __hash__(self):
        return hash((self.excel_prop.name, self.cell.coordinate, self.issue))

    def __key(self):
        return self.excel_prop.name, self.cell.coordinate, self.issue

    def __eq__(self, other):
        if isinstance(other, TableCell):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, TableCell):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, TableCell):
            return self.row < other.row
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, TableCell):
            return self.row > other.row
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, TableCell):
            return self.row <= other.row
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, TableCell):
            return self.row >= other.row
        else:
            return NotImplemented

    @property
    def ws(self):
        return self.excel_prop.ws

    @property
    def row(self):
        return self.cell.row

    def _get_shift_col_idx(self, column: str) -> int:
        return column_index_from_string(column) - self.cell.col_idx

    def _shift_cell(self, value: int) -> Optional[Cell]:
        col_idx = self.cell.col_idx + value
        if col_idx > 1:
            column_letter = get_column_letter(col_idx)
            return self.ws[f"{column_letter}{self.row}"]
        else:
            print(f"ValueError, the shift {value} is out of bounds.")
            return None

    @property
    def state(self):
        for state in self.excel_prop.dict_headers_short.keys():
            if self.row in self.excel_prop.list_state_item(state):
                return state
            else:
                continue
        return None

    def _commentary(self):
        return self._shift_cell(self._get_shift_col_idx("NT")).value

    def _summary(self):
        return self._shift_cell(1).value

    def _deadline(self):
        return self._shift_cell(2).value

    def _parent(self):
        return self._shift_cell(-1).value

    def pyxl_row(self):
        return self.issue, self.state, self._summary(), self._parent(), self._deadline()

    def __cell_range(self):
        return self.excel_prop.cell_in_range(f"G{self.row}", f"NR{self.row}")

    def __pyxl_cells(self) -> list[Cell]:
        return [cell for cell in self.__cell_range() if cell.value is not None]

    def pyxl_work_items(self):
        return [self._mapping_cell_work_item(cell) for cell in self.__pyxl_cells()]

    def pyxl_cell_last(self) -> Cell:
        max_column = max(cell.column_letter for cell in self.__pyxl_cells())
        return self.ws[f"{max_column}{self.row}"]

    def pyxl_work_item_last(self):
        cell: Cell = self.pyxl_cell_last()
        return self._mapping_cell_work_item(cell)

    def set_pyxl_work_item_style(self, style_name: str, cell: Cell):
        cell._style = self.excel_prop.styles.set_style(style_name, cell)

    def _mapping_cell_work_item(self, cell: Cell) -> tuple[str, datetime.date, Decimal]:
        date = self.excel_prop.get_date_by_cell(cell)
        return self.issue, date, Decimal(cell.value).normalize()

    def _mapping_work_item_cell(self, work_item: tuple[str, datetime.date, Decimal]) -> Cell:
        _, date, _ = work_item
        column = self.excel_prop.get_column_by_date(date)
        return self.ws[f"{column}{self.row}"]

    def compare_cell_work_item(self, cell: Cell, work_item: tuple[str, datetime.date, Decimal]):
        if cell not in self.__pyxl_cells() or work_item not in self.pyxl_work_items():
            return False
        work_item_cell = self._mapping_work_item_cell(work_item)
        return cell.coordinate == work_item_cell.coordinate

    def add_work_item(self, date: datetime.date, spent_time: Decimal):
        cell = self._mapping_work_item_cell((self.issue, date, spent_time))
        cell.data_type = "n"
        cell.value = spent_time


def main():
    pass


if __name__ == "__main__":
    main()
