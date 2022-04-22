import datetime
from copy import copy
from openpyxl.styles.cell_style import CellStyle
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import get_column_letter, rows_from_range, coordinate_from_string, column_index_from_string
from _style_work_item import _StyleWorkItemList


class ConstDefaultWs:
    __doc__ = """"""
    # style_name: (rus_name, cell_style_coordinate, cell_legend_coordinate
    dict_legend = {
        'weekend': ('выходные', 'B21', 'C21'), 'deadline': ('дедлайн', 'B22', 'C22'), 'done': ('done', 'B23', 'C23'),
        'active': ('active', 'B24', 'C24'), 'test': ('test', 'B25', 'C25'),
        'going_start': ('планирую начать', 'B26', 'C26'), 'paused': ('paused', 'B27', 'C27'),
        'verified_closed': ('verified, closed', 'B28', 'C28'), 'going_finish': ('планирую завершить', 'B29', 'C29'),
        'sick': ('больничный', 'B30', 'C30'), 'vacation': ('отпуск', 'B31', 'C31')
    }
    # title_name: (rus_name, cell_title_coordinate)
    dict_titles = {
        'parent': ('РОД. ЗАДАЧА', 'B2'), 'name': ('ЗАДАЧА', 'C2'), 'summary': ('ОПИСАНИЕ', 'D2'),
        'deadline': ('DEADLINE', 'E2'), 'sum': ('Σ', 'NS2'), 'commentary': ('ПРИМЕЧАНИЕ', 'NT2')
    }
    # month_name: (rus_name, cell_title_coordinate, num_days)
    dict_month_ranges: dict[str, tuple[str, str, int]] = {
        'january': ('ЯНВАРЬ', 'F1', 31), 'february': ('ФЕВРАЛЬ', 'AL1', 28), 'march': ('МАРТ', 'BO1', 31),
        'april': ('АПРЕЛЬ', 'CU1', 30), 'may': ('МАЙ', 'DZ1', 31), 'june': ('ИЮНЬ', 'FF1', 30),
        'july': ('ИЮЛЬ', 'GK1', 31), 'august': ('АВГУСТ', 'HQ1', 31), 'september': ('СЕНТЯБРЬ', 'IW1', 30),
        'october': ('ОКТЯБРЬ', 'KB1', 31), 'november': ('НОЯБРЬ', 'LH1', 30), 'december': ('ДЕКАБРЬ', 'MM1', 31)
    }

    cells_headers: tuple[tuple[int, str]] = ((3, 'Active'), (7, 'New/Paused'), (11, 'Active/Done'), (15, 'Verified'))
    # holidays
    yy: int = datetime.date.today().year
    holidays = (
        datetime.date(yy, 1, 1), datetime.date(yy, 1, 2), datetime.date(yy, 1, 3), datetime.date(yy, 1, 4),
        datetime.date(yy, 1, 5), datetime.date(yy, 1, 6), datetime.date(yy, 1, 7), datetime.date(yy, 2, 23),
        datetime.date(yy, 3, 7), datetime.date(yy, 3, 8), datetime.date(yy, 5, 1), datetime.date(yy, 5, 2),
        datetime.date(yy, 5, 3), datetime.date(yy, 5, 8), datetime.date(yy, 5, 9), datetime.date(yy, 5, 10),
        datetime.date(yy, 6, 12), datetime.date(yy, 6, 13), datetime.date(yy, 11, 4), datetime.date(yy, 12, 31)
    )
    # for set_fill_color:
    # type_fill: str, fill_color: str, tint: float = None, theme: int = None
    dict_months_colors = {
        'january': ('tmp', 'FF0297CC', None, None), 'february': ('tmp', 'FF0BA6B6', None, None),
        'march': ('tmp', 'FF3AAA66', None, None), 'april': ('tmp', 'FF8BBD36', None, None),
        'may': ('tmp', 'FFD0CA04', None, None), 'june': ('tmp', 'FFF9AD01', None, None),
        'july': ('tmp', 'FFF08002', None, None), 'august': ('tmp', 'FFE94442', None, None),
        'september': ('tmp', 'FFCF687D', None, None), 'october': ('tmp', 'FF98668B', None, None),
        'november': ('tmp', 'FF697FB9', None, None), 'december': ('tmp', 'FF0078A9', None, None)
    }
    # month title StyleCell values
    # ['january', 'february', 'march', 'april', 'may', 'june', 'july',
    # 'august', 'september', 'october', 'november', 'december']
    dict_month_title_styles: dict[str, tuple] = dict()
    # month header StyleCell values
    dict_month_header_styles: dict[str, tuple] = dict()
    # StyleCell values
    dict_style_cells: dict[str, tuple] = dict()

def month_cell_periods():
    """Merges cells for the month title."""
    start_cells = [add_column(month_coord, 1) for month_params in ConstDefaultWs.dict_month_ranges.values()
                   for _, month_coord, _ in month_params]
    end_cells = [add_column(month_coord, num_days) for month_params in ConstDefaultWs.dict_month_ranges.values()
                 for _, month_coord, num_days in month_params]
    return [f"{start_cell}:{end_cell}" for start_cell, end_cell in zip(start_cells, end_cells)]


def add_column(coord: str, add_value: int):
    """
    Finds the cell in the row that is N columns to the left/right.\n
    :param coord: the base cell coordinate, str
    :param add_value: the number of columns with the sign, int
    :return: the new cell coordinate of the str value.
    """
    column, row = coordinate_from_string(coord)
    col_idx = column_index_from_string(column)
    if add_value < 0 and col_idx + add_value < 1:
        print('The incorrect work of the add_column method.')
        return coord
    add_col_idx = col_idx + add_value
    add_column = get_column_letter(add_col_idx).upper()
    return f'{add_column}{row}'


class WorksheetDefault:
    __doc__ = """"""

    def __init__(self, wb: Workbook, ws: Worksheet, styles: _StyleWorkItemList):
        self.wb = wb
        self.ws = ws
        self.styles = styles

    def __str__(self):
        return f"Workbook: {self.wb}, Worksheet: {self.ws}"

    def __repr__(self):
        return f"Work"


    def __hash__(self):
        return hash((self.wb.properties.name, self.ws.title))

    def __key(self):
        return self.wb.properties.name, self.ws.title

    def __eq__(self, other):
        if isinstance(other, WorksheetDefault):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, WorksheetDefault):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __contains__(self, item):
        return item in self.styles



    def set_style_cell(self, coord: str, style_name: str):
        """Alias for the self.const.set_style_cell."""
        style = self.styles.get_style(style_name)
        self.ws[f'{coord}']._style = copy(style)
        return style

    def set_dates(self):
        """Specifies the dates in row 1."""
        for index, month_params in enumerate(ConstDefaultWs.dict_month_ranges.values()):
            _, coord, num_days = month_params
            start_col_idx = self.column_col_idx(coord)
            year = datetime.date.today().year
            month = index + 1

            for day in range(1, num_days + 1):
                col_idx = start_col_idx + day
                cell_coord = f'{get_column_letter(col_idx)}1'
                self.ws[f'{cell_coord}'].value = datetime.date(year=year, month=month, day=day)

    def set_month_names(self):
        """Specifies the month names."""
        for month, month_params in ConstDefaultWs.dict_month_ranges.items():
            rus_name, coord, _ = month_params
            self.ws[f'{coord}'].value = rus_name
            self.ws[f'{coord}']._style = self.set_style_cell(coord, month)

    def month_cell_merge(self):
        """Merges cells for the month title."""
        for period in month_cell_periods():
            self.ws.merge_cells(period)

    def set_month_title(self):
        """Defines the month titles."""
        for index, coord in enumerate(ConstDefaultWs.month_cell_periods_start()):
            self.ws[f'{coord}'].value = self.cells_month[index]
            self.ws[f'{coord}']._style = self.set_style_cell(coord, ConstDefaultWs.dict_month_title_styles[index].name)

    def set_default(self):
        """Applies the basic style for the whole table."""
        for row in rows_from_range(f'A1:NT18'):
            for coord in row:
                cell: Cell = self.ws[f'{coord}']
                cell._style = self.set_style_cell(coord, 'basic')

    def set_weekends(self):
        """Applies the weekend style."""
        for column_letter in self.cols_weekend:
            for row in self.rows_weekend:
                coord = f'{column_letter}{row}'
                cell: Cell = self.ws[f'{coord}']
                cell._style = self.set_style_cell(coord=coord, style_name='weekend')

    def set_headers(self):
        """Applies the headers."""
        for row, value in ConstDefaultWs.cells_headers:
            # merge the cells
            self.ws.merge_cells(f'B{row}:E{row}')

            cell: Cell = self.ws[f'B{row}']
            cell.value = value
            cell._style = self.set_style_cell(cell.coordinate, 'headers')

    def set_headers_row(self):
        """Applies the headers row."""
        for row, value in ConstDefaultWs.cells_headers:
            cell_range: tuple[Cell] = self.ws[f'F{row}:NT{row}']
            row_range: tuple[Cell]
            cell: Cell
            for row_range in cell_range:
                for cell in row_range:
                    cell._style = self.set_style_cell(cell.coordinate, 'headers')

    def set_title(self):
        """Defines the title row."""
        for coord, title in zip(self.title_coord, self.titles):
            cell: Cell = self.ws[f'{coord}']
            cell.value = title
            cell._style = self.set_style_cell(coord=coord, style_name='title')

    def set_legend(self):
        """Defines the legend."""
        self.ws.merge_cells('B21:C21')
        self.ws['B21'].value = 'Легенда'

        for index, style_name in enumerate(ConstDefaultWs.dict_legend):
            row = index + 22
            self.ws[f'C{row}'].value = style_name
            cell: Cell = self.ws[f'B{row}']
            cell._style = self.set_style_cell(coord=cell.coordinate, style_name=self.const.const_styles[index])

    def column_col_idx(self, coord: str) -> int:
        """
        Converts the cell coord to the column index.
        :param coord: the cell coord, str
        :return: the col_idx of the int type.
        """
        cell: Cell = self.ws[f'{coord}']
        return cell.col_idx

    def set_table(self):
        """Defines the cell styles in the table."""
        cell: Cell
        row: tuple[Cell]
        for row in self.ws['B1:NT18']:
            for cell in row:
                cell._style = self.set_style_cell(cell.coordinate, 'table')
                # 'table'

    def set_month_ranges(self):
        for
    """
        dict_month_ranges: dict[str, tuple[str, str, int]] = {
        'january': ('ЯНВАРЬ', 'F1', 31), 'february': ('ФЕВРАЛЬ', 'AL1', 28), 'march': ('МАРТ', 'BO1', 31),
        'april': ('АПРЕЛЬ', 'CU1', 30), 'may': ('МАЙ', 'DZ1', 31), 'june': ('ИЮНЬ', 'FF1', 30),
        'july': ('ИЮЛЬ', 'GK1', 31), 'august': ('АВГУСТ', 'HQ1', 31), 'september': ('СЕНТЯБРЬ', 'IW1', 30),
        'october': ('ОКТЯБРЬ', 'KB1', 31), 'november': ('НОЯБРЬ', 'LH1', 30), 'december': ('ДЕКАБРЬ', 'MM1', 31)
    }
    """

def main():
    pass


if __name__ == '__main__':
    main()
