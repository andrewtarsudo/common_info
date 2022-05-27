import collections
from typing import Optional, Union, Any
import datetime
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter, column_index_from_string
from decimal import Decimal
from _style_work_item import _StyleWorkItemList
from copy import copy


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
        dict_headers --- the dictionary of the states and indexes;\n
        dict_headers_short --- the dictionary of the issue states and indexes;\n
        dict_attr_column --- the dictionary of the issue attributes and columns;\n
        dict_state_style --- the dictionary of the states and cell styles;\n
        dict_state_priority --- the dictionary of the states and priorities;\n

    Class params:
        dict_table_cell --- the dictionary of the TableCell instances;\n

    Params:
        ws --- the worksheet;\n
        name --- the instance name;\n
        styles --- the _StyleWorkItemList instance;\n

    Properties:
        headers --- the header cells;\n
        headers_row --- the header cell rows;\n
        cell_states --- the dictionary of the cell coordinates and states;\n
        table_cells --- the cells for the TableCell instances;\n
        table_cell_names --- the issue names;\n

    Functions:
        get_column_by_date(date) --- get the column letter for the specified date;\n
        cell_in_range(start_coord, end_coord) --- generate the cells in the range;\n
        _check_empty(item) --- verify if the Cell, Cell.coordinate, or Cell.row is empty;\n
        _empty_rows() --- delete all empty rows except for the pre-headers;\n
        new_row(state) --- get the row for the new issue of the state;\n
        get_row_by_name(issue) --- get the row by the issue name;\n
        replace_cell(*, from_, to_) --- replace the cell attribute values to another cell;\n
        add_work_item() --- add the work item to the table;\n
        get_date_by_cell(cell) --- get the date associated with the cell;\n
        __index(state) --- get the state index;\n
        table_cell_items() --- get the TableCell instances;\n
        pre_processing() --- pre-process the table to get rid of empty rows and repeating issues;\n
    """
    dict_headers = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3, 'Легенда': 4}
    dict_headers_short = {'Active': 0, 'New/Paused': 1, 'Done/Test': 2, 'Verified': 3}
    dict_attr_column = {"parent": "B", "issue": "C", "summary": "D", "deadline": "E", "commentary": "NT"}
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
    dict_state_priority: dict[str, int] = {"Active": 30, "New/Paused": 10, "Done/Test": 20, "Verified": 40}
    dict_table_cell = dict()

    def __init__(self, ws: Worksheet, name: str, styles: _StyleWorkItemList):
        self.ws = ws
        self.name = name
        self.styles = styles

    def __str__(self):
        return f"Worksheet: {self.ws.title}, name: {self.name}"

    def __repr__(self):
        return f"ExcelProp(ws={self.ws}, name={self.name})"

    def __format__(self, format_spec):
        if format_spec == "base":
            return str(self)
        elif format_spec == "row_equal":
            return repr(self)
        else:
            return f"{self.name}"

    def __hash__(self):
        return hash((self.ws, self.name))

    def __key(self):
        return self.ws, self.name

    def __eq__(self, other):
        if isinstance(other, ExcelProp):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ExcelProp):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def get_column_by_date(self, date: datetime.date) -> str:
        """
        Get the column letter for the specified date.

        :param date: the date
        :type date: datetime.date
        :return: the column_letter.
        :rtype: str
        """
        cell: Cell
        for cell in self.cell_in_range("G1", "NR1"):
            if convert_datetime_date(cell.value) == date:
                return cell.column_letter

    def cell_in_range(self, start_coord: str, end_coord: str):
        """
        Convert the cell range to the cell generator in the range.

        :param str start_coord: the start cell coordinates
        :param str end_coord: the end cell coordinates
        :return: the generator of cells.
        """
        if check_coord(coord=start_coord) and check_coord(coord=end_coord):
            min_row, max_row, min_col, max_col = range_coord(start_coord=start_coord, end_coord=end_coord)
            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    coord = f'{get_column_letter(col)}{row}'
                    cell: Cell = self.ws[coord]
                    yield cell

    @property
    def headers(self) -> list[Cell]:
        """
        Get the header cells.

        :return: the cells.
        :rtype: list[Cell]
        """
        end_coord = f"B{self.ws.max_row}"
        return [cell for cell in self.cell_in_range("B3", end_coord) if cell.value in ExcelProp.dict_headers.keys()]

    @property
    def headers_row(self) -> list[int]:
        """
        Get the header row values.

        :return: the list of header rows.
        :rtype: list[int]
        """
        return [header.row for header in self.headers]

    def _check_empty(self, item: Union[int, str, Cell]) -> bool:
        """
        Verify if the cell, cell coordinates, or cell row is empty.

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

    def _empty_rows(self):
        """Delete all empty rows except for the pre-headers."""
        list_empty = []
        for state in self.dict_headers_short.keys():
            low_limit = self.headers_row[self.__index(state)] + 1
            high_limit = self.headers_row[self.__index(state) + 1] - 1
            for row in range(low_limit, high_limit):
                if self._check_empty(row):
                    list_empty.append(row)
        print(list_empty)
        for empty_row in sorted(list_empty, reverse=True):
            self.ws.delete_rows(empty_row)

    def new_row(self, state: str) -> int:
        """
        Get the row for the new issue in the table.

        :param str state: the issue state
        :return: the row number.
        :rtype: int
        """
        return self.headers_row[self.__index(state) + 1] - 1

    def replace_cell(self, *, from_: Union[Cell, str], to_: Optional[Union[Cell, str]] = None):
        """
        Replace the cell attribute values to another cell. If to_ is None, the values are deleted.

        :param from_: the original cell or cell coordinates
        :type from_: Cell or str
        :param to_: the destination cell or cell coordinates
        :type to_: Cell or str or None
        :return: None.
        """
        cell_proxy: Optional[Cell]
        cell_base: Cell
        # if the cell coordinates
        if isinstance(from_, str):
            cell_base = self.ws[f"{from_}"]
        # if the cell
        else:
            cell_base = from_
        # if the destination cell exists
        if to_ is not None:
            if isinstance(to_, str):
                cell_proxy = self.ws[f"{to_}"]
            else:
                cell_proxy = to_
            # copy all required attribute values
            # if the destination cell is empty
            if cell_proxy.value is None:
                cell_proxy.value = cell_base.value
            # if the destination cell has some value
            else:
                cell_proxy.value += cell_base.value
            cell_proxy._style = copy(cell_base.style)
        # set the default cell attribute values
        cell_base.value = None
        self.styles.set_style("basic", cell_base)

    def add_work_item(self, work_item: tuple[str, datetime.date, Union[int, Decimal]]):
        """
        Add the work item to the table.

        issue_name: str, date: datetime.date, spent_time: Union[int, Decimal]
        :param work_item: the work item to add
        :type work_item: tuple[str, datetime.date, Decimal or int]
        :return: None.
        """
        issue_name, *_ = work_item
        self.dict_table_cell[issue_name].add_work_item(work_item)

    def get_date_by_cell(self, cell: Cell) -> Optional[datetime.date]:
        """
        Get the date associated with the cell.

        :param cell: the table cell
        :type cell: Cell
        :return: the date.
        :rtype: datetime.date or None
        """
        column = cell.column_letter
        raw_date = self.ws[f"{column}1"].value
        return convert_datetime_date(raw_date)

    def __index(self, state: str) -> int:
        """
        Get the state index.

        :param str state: the state
        :return: the header index.
        :rtype: int
        """
        return self.dict_headers_short[state]

    @property
    def cell_states(self):
        """
        Get the dictionary of the cell coordinates and states.

        :return: the cell coordinates and state mapping.
        :rtype: dict[str, str]
        """
        dict_cell_states: dict[str, str] = dict()
        for state in self.dict_headers_short.keys():
            start_row = self.headers_row[self.__index(state)] + 1
            end_row = self.headers_row[self.__index(state) + 1]
            start_coord = f"C{start_row}"
            end_coord = f"C{end_row}"
            for cell in self.cell_in_range(start_coord, end_coord):
                dict_cell_states[cell.coordinate] = state
        return dict_cell_states

    @property
    def table_cells(self) -> list[Cell]:
        """
        Get the cells for the TableCell instances.

        :return: the cells.
        :rtype: list[Cell]
        """
        return [self.ws[f"{coord}"] for coord in self.cell_states if self.ws[f"{coord}"].value is not None]

    def table_cell_items(self):
        """
        Get the TableCell instances.

        :return: the TableCell instances.
        :rtype: list[TableCell]
        """
        return [TableCell(self, cell) for cell in self.table_cells]

    def table_cell_issue(self, table_base: Union[int, Cell, str]):
        """
        Get the TableCell instance based on the row, cell, or issue name.

        :param table_base: the object to link to the TableCell instance
        :type table_base: int or Cell or str
        :return: the TableCell instance.
        :rtype: TableCell or None
        """
        if isinstance(table_base, int):
            cell = self.ws[f"C{table_base}"]
            return TableCell(self, cell)
        elif isinstance(table_base, str):
            return self.dict_table_cell[table_base]
        elif isinstance(table_base, Cell):
            return TableCell(self, table_base)
        else:
            print(f"Something went wrong. Table base: {table_base}, type: {type(table_base)}.")
            return None

    def table_cell_names(self) -> list[str]:
        """
        Get the issue names.

        :return: the issue names.
        :rtype: list[str]
        """
        return [cell.value for cell in self.table_cells]

    def pre_processing(self):
        """Pre-process the table to get rid of empty rows and repeating issues."""
        counter = collections.Counter(self.table_cell_names())
        non_unique = [key for key, value in counter.items() if value > 1]
        for issue in non_unique:
            row_eq = _RowEqual(self, issue)
            row_eq.join_cells()
        self._empty_rows()

    def add_issue(self, issue_params: tuple[str, str, str, Optional[str], Optional[datetime.date]]):
        """
        Add the issue to the table.\n

        issue, state, summary, parent, deadline

        :param issue_params: the values to add to the table
        :type issue_params: tuple[str, str, str, Optional[str], Optional[datetime.date]]
        :return: None.
        """
        issue_name, issue_state, issue_summary, issue_parent, issue_deadline = issue_params
        # verify the issue name is not in the table
        if issue_name in self.table_cell_names:
            print(f"The issue name {issue_name} is already in the table. It is modified.")
            return self.modify_issue(issue_params)
        # prepare the new row
        add_row = self.new_row(issue_state)
        self.ws.insert_rows(add_row)
        # add the values to the associated cells
        attrs = ["parent", "issue", "summary", "deadline"]
        values = [issue_parent, issue_name, issue_summary, issue_deadline]
        self._parse_attr_seq(attrs, values, add_row)

    def _parse_attr(self, attr: str, value, row: int):
        """
        Add the issue attribute value to the table.

        :param str attr: the attribute name
        :param value: the attribute value
        :param int row: the row in the table
        :return: None.
        """
        if attr in self.dict_attr_column.keys():
            if value is not None:
                column_letter = self.dict_attr_column[attr]
                self.ws[f"{column_letter}{row}"].value = value
            else:
                print("The None value is not assigned.")

    def _parse_attr_seq(self, attrs: list[str], values: list[str], row: int):
        if len(attrs) != len(values):
            print("Improper lengths.")
            return
        for attr, value in zip(attrs, values):
            self._parse_attr(attr, value, row)

    def modify_issue(self, issue_params: tuple[str, str, str, Optional[str], Optional[datetime.date]]):
        issue_name, issue_state, issue_summary, issue_parent, issue_deadline = issue_params
        if issue_name not in self.table_cell_names():
            print(f"The issue {issue_name} is not in the table. It is added.")
            return self.add_issue(issue_params)
        table_cell = self.table_cell_issue(issue_name)
        row = table_cell.row
        if table_cell.parent != issue_parent:
            self._parse_attr("parent", issue_parent, row)
        if table_cell.summary() != issue_summary:
            self._parse_attr("summary", issue_summary, row)
        if table_cell.deadline() != issue_deadline:
            self._parse_attr("deadline", issue_deadline, row)
        if table_cell.state != issue_state:
            add_row = self.new_row(issue_state)
            for cell in self.cell_in_range(f"B{row}", f"NT{row}"):
                self.replace_cell(from_=cell, to_=self.ws[f"{cell.column_letter}{add_row}"])
            self.ws.delete_rows(row)


class TableCell:
    """
    Define the table row.

    Params:
        excel_prop --- the ExcelProp instance;\n
        cell --- the base cell;\n
        issue --- the base cell value;\n

    Properties:
        ws --- the worksheet;\n
        row --- the row;\n
        state --- the state;\n
        cell_last --- the last work item cell;\n
        work_item_last --- the last work item;\n

    Functions:
        _shift_col_idx(column) --- get the shift between the column and the base cell;\n
        _shift_cell(shift) --- get the shifted cell in the same row;\n
        commentary() --- get the commentary;\n
        summary() --- get the summary;\n
        deadline() --- get the deadline;\n
        parent() --- get the parent issue name;\n
        pyxl_row() --- get the values to operate with the Issue instances;\n
        _cell_range() --- generate the cells in the range;\n
        _pyxl_cells() --- get the work item cells;\n
        work_items() --- get the work items;\n
        set_cell_style(style_name, cell) --- set the style to the cell;\n
        _mapping_cell_work_item(cell) --- convert the cell to the work item;\n
        _mapping_work_item_cell(work_item) --- convert the work item to the cell;\n
        compare_cell_work_item(cell, work_item) --- verify the coincidence of the cell and work item;\n
        add_work_item(work_item) --- add the work item to the row;
        _proper_cell_style(cell) --- get the cell style based on the state;\n
        _proper_work_item_style(work_item) --- get the work item style based on the state;\n
    """
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
    def ws(self) -> Worksheet:
        """
        Get the ExcelProp worksheet.

        :return: the worksheet.
        :rtype: Worksheet
        """
        return self.excel_prop.ws

    @property
    def row(self) -> int:
        """
        Get the base cell row.

        :return: the cell row.
        :rtype: int
        """
        return self.cell.row

    def _shift_col_idx(self, column: str) -> int:
        """
        Get the difference between the column and the base cell.

        :param str column: the column letter
        :return: the column shift.
        :rtype: int
        """
        return column_index_from_string(column) - self.cell.col_idx

    def _shift_cell(self, shift: int) -> Optional[Cell]:
        """
        Get the shifted cell in the same row.

        :param int shift: the cell shift
        :return: the shifted cell.
        :rtype: Cell or None
        """
        col_idx = self.cell.col_idx + shift
        if col_idx >= 1:
            column_letter = get_column_letter(col_idx)
            return self.ws[f"{column_letter}{self.row}"]
        else:
            print(f"ValueError, the shift {shift} is out of bounds.")
            return None

    @property
    def state(self) -> str:
        """
        Get the issue state.

        :return: the state.
        :rtype: str
        """
        return self.excel_prop.cell_states[self.cell.coordinate]

    def commentary(self) -> str:
        """
        Get the issue commentary.

        :return: the commentary.
        :rtype: str
        """
        return self._shift_cell(self._shift_col_idx("NT")).value

    def summary(self) -> str:
        """
        Get the issue summary.

        :return: the summary.
        :rtype: str
        """
        return self._shift_cell(1).value

    def deadline(self) -> Optional[datetime.date]:
        """
        Get the issue deadline if exists.

        :return: the deadline.
        :rtype: datetime.date or None
        """
        return self._shift_cell(2).value

    def parent(self):
        """
        Get the parent issue name if exists.

        :return: the parent issue name.
        :rtype: str
        """
        return self._shift_cell(-1).value

    def pyxl_row(self) -> tuple[str, str, str, Optional[str], Optional[datetime.date]]:
        """
        Get the values to operate with the Issue instances.

        :return: the attribute values.
        :rtype: tuple[str, str, str, Optional[str], Optional[datetime.date]]
        """
        return self.issue, self.state, self.summary(), self.parent(), self.deadline()

    def _cell_range(self):
        """
        Specify the cell generator for the range.

        :return: iterating through the cells.
        """
        return self.excel_prop.cell_in_range(f"G{self.row}", f"NR{self.row}")

    def _pyxl_cells(self) -> list[Cell]:
        """
        Get the work item cells.

        :return: the cells.
        :rtype: list[Cell]
        """
        return [cell for cell in self._cell_range() if cell.value is not None]

    def work_items(self) -> list[tuple[str, datetime.date, Decimal]]:
        """
        Get the work items.

        :return: the work items.
        :rtype: list[tuple[str, datetime.date, Decimal]]
        """
        return [self._mapping_cell_work_item(cell) for cell in self._pyxl_cells()]

    @property
    def cell_last(self) -> Cell:
        """
        Get the last work item cell.

        :return: the last work item cell.
        :rtype: Cell
        """
        max_column = max(cell.column_letter for cell in self._pyxl_cells())
        return self.ws[f"{max_column}{self.row}"]

    @property
    def work_item_last(self) -> tuple[str, datetime.date, Decimal]:
        """
        Get the last work item.

        :return: the work item.
        :rtype: tuple[str, datetime.date, Decimal]
        """
        cell: Cell = self.cell_last
        return self._mapping_cell_work_item(cell)

    def set_cell_style(self, style_name: str, cell: Cell):
        """
        Set the style to the cell.

        :param str style_name: the style name
        :param cell: the cell
        :type cell: Cell
        :return: None.
        """
        self.excel_prop.styles.set_style(style_name, cell)

    def _mapping_cell_work_item(self, cell: Cell) -> tuple[str, datetime.date, Decimal]:
        """
        Convert the cell to the work item.

        :param cell: the cell
        :type cell: Cell
        :return: the work item.
        :rtype: tuple[str, datetime.date, Decimal]
        """
        date = self.excel_prop.get_date_by_cell(cell)
        return self.issue, date, Decimal(cell.value).normalize()

    def _mapping_work_item_cell(self, work_item: tuple[str, datetime.date, Decimal]) -> Cell:
        """
        Convert the work item to the cell.

        :param work_item: the work item
        :type work_item: tuple[str, datetime.date, Decimal]
        :return: the cell.
        :rtype: Cell
        """
        _, date, _ = work_item
        column = self.excel_prop.get_column_by_date(date)
        return self.ws[f"{column}{self.row}"]

    def compare_cell_work_item(self, cell: Cell, work_item: tuple[str, datetime.date, Decimal]) -> bool:
        """
        Verify the cell and the work item are the same instance.

        :param cell: the cell
        :type cell: Cell
        :param work_item: the work item
        :type work_item: tuple[str, datetime.date, Decimal]
        :return: the verification flag.
        :rtype: bool
        """
        if cell not in self._pyxl_cells() or work_item not in self.work_items():
            return False
        work_item_cell = self._mapping_work_item_cell(work_item)
        return cell.coordinate == work_item_cell.coordinate

    def add_work_item(self, work_item: tuple[str, datetime.date, Decimal]):
        """
        Add the work item to the row.

        :param work_item: the work item
        :type work_item: tuple[str, datetime.date, Decimal]
        :return: None.
        """
        _, date, spent_time = work_item
        cell = self._mapping_work_item_cell((self.issue, date, spent_time))
        cell.data_type = "n"
        cell.value = spent_time

    def _proper_cell_style(self, cell: Cell) -> str:
        """
        Get the cell style based on the state.

        :param cell: the cell
        :type cell: Cell
        :return: the style name.
        :rtype: str
        """
        if cell not in self._pyxl_cells():
            return cell.style.name
        elif self.excel_prop.get_date_by_cell(cell) == self.deadline():
            return "deadline"
        elif cell != self.cell_last:
            return "active"
        elif self.state is not None:
            return self.excel_prop.dict_state_style[self.state]
        else:
            return "basic"

    def _proper_work_item_style(self, work_item: tuple[str, datetime.date, Decimal]) -> str:
        """
        Get the proper work item style based on the state.

        :param work_item: the work item
        :type work_item: tuple[str, datetime.date, Decimal]
        :return: the style name
        :rtype: str
        """
        _, date, spent_time = work_item
        cell = self._mapping_work_item_cell((self.issue, date, spent_time))
        return self._proper_cell_style(cell)


class _RowEqual:
    """
    Define the instance to work with the issues having the same names.

    Params:
        excel_prop --- the ExcelProp instance;\n
        issue --- the issue name;\n

    Properties:
        cells --- the cells with the same issue names;\n
        dict_issues --- the dictionary of the issue cells and state priorities;\n
        max_priority --- the maximum priority of the issue states;\n

    Functions:
        work_item_cells() --- get the cells to join;\n
        max_prior_min_row() --- get the minimum row if the issues have the same states;\n
        cell_final() --- get the final cell to keep in the table;\n
        join_cells() --- join the cells into the one issue;\n
    """
    def __init__(self, excel_prop: ExcelProp, issue: str):
        self.excel_prop = excel_prop
        self.issue = issue

    def __str__(self):
        cell_string = ", ".join([cell.coordinate for cell in self.cells])
        return f"_RowEqual: issue name - {self.issue},\ncells - {cell_string}"

    def __repr__(self):
        return f"_RowEqual({format(self.excel_prop, 'row_equal')}, {self.issue})"

    def __len__(self):
        return len(self.cells)

    def __bool__(self):
        return len(self.cells) > 1

    def __contains__(self, item):
        return item in self.cells or item in self.work_item_cells()

    def __iter__(self):
        return (cell for cell in self.cells)

    @property
    def cells(self) -> list[Cell]:
        """
        Get the issue cells with the same names.

        :return: the cells.
        :rtype: list[Cell]
        """
        return [cell for cell in self.excel_prop.table_cells if cell.value == self.issue]

    @property
    def dict_issues(self) -> dict[Cell, int]:
        """
        Get the dictionary of the issue cells and state priorities.

        :return: the cell and state priority mapping.
        :rtype: dict[Cell, int]
        """
        dict_cell_priority: dict[Cell, int] = dict()
        for cell in self.cells:
            state = self.excel_prop.cell_states[cell.coordinate]
            dict_cell_priority[cell] = self.excel_prop.dict_state_priority[state]
        return dict_cell_priority

    def work_item_cells(self) -> list[Cell]:
        """
        Get the work item cells to join.

        :return: the work item cells.
        :rtype: list[Cell]
        """
        work_cells: list[Cell] = []
        for cell in self.cells:
            if cell == self.cell_final():
                continue
            else:
                for item in self.excel_prop.cell_in_range(f"G{cell.row}", f"NR{cell.row}"):
                    if item.value is not None:
                        work_cells.append(item)
                    else:
                        continue
        return work_cells

    @property
    def max_priority(self) -> int:
        """
        Get the maximum priority of the issue states.

        :return: the maximum priority.
        :rtype: int
        """
        return max(priority for priority in self.dict_issues.values())

    def max_prior_min_row(self) -> int:
        """
        Get the minimum row if the issues have the same state.

        :return: the minimum row.
        :rtype: int
        """
        return min(cell.row for cell, priority in self.dict_issues.items() if priority == self.max_priority)

    def cell_final(self) -> Cell:
        """
        Get the final cell to keep.

        :return: the cell
        :rtype: Cell
        """
        for cell in self.cells:
            if cell.row == self.max_prior_min_row():
                return cell

    def join_cells(self):
        """Join the work items to the final issue."""
        row_final = self.cell_final().row
        for cell in self.work_item_cells():
            self.excel_prop.replace_cell(from_=cell, to_=f"{cell.column_letter}{row_final}")
        for issue_cell in self.cells:
            if issue_cell != self.cell_final():
                row = issue_cell.row
                for column in ("B", "C", "D", "E"):
                    self.excel_prop.replace_cell(from_=f"{column}{row}")


def main():
    pass


if __name__ == "__main__":
    main()
