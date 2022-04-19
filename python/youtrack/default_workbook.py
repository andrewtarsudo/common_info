import datetime
from copy import copy
from openpyxl.styles.cell_style import CellStyle
from const import ConstDefault, Const
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from openpyxl.utils.cell import get_column_letter, rows_from_range
from style_cell import StyleCell, StyleList
from attrs import define, field, validators, converters


validators_list = validators.deep_iterable(validators.instance_of(StyleCell), validators.instance_of(StyleList))


@define(repr=True, init=True, str=True)
class WorksheetDefault:
    wb: Workbook = field(repr=False, init=True, eq=True, validator=validators.instance_of(Workbook))
    ws: Worksheet = field(repr=False, init=True, eq=True, validator=validators.instance_of(Worksheet))
    styles: StyleList = field(repr=False, init=True, eq=False, validator=validators_list)

    def set_style_cell(self, coord: str, style_name: str):
        """Alias for the self.const.set_style_cell."""
        style = self.styles.return_style(style_name=style_name)
        self.ws[f'{coord}']._style = copy(style)
        return style

    def set_dates(self):
        """Specifies the dates in row 1."""
        for index, month_params in enumerate(ConstDefault.dict_month_ranges.values()):
            _, coord, num_days = month_params
            start_col_idx = self.column_col_idx(coord=coord)
            year = datetime.date.today().year
            month = index + 1

            for day in range(1, num_days + 1):
                col_idx = start_col_idx + day
                cell_coord = f'{get_column_letter(col_idx)}1'
                self.ws[f'{cell_coord}'].value = datetime.date(year=year, month=month, day=day)

    def set_month_names(self):
        """Specifies the month names."""
        for month, month_params in ConstDefault.dict_month_ranges.items():
            rus_name, coord, _ = month_params
            self.ws[f'{coord}'].value = rus_name
            self.ws[f'{coord}']._style = self.styles.return_style(month)

    def month_cell_merge(self):
        """Merges cells for the month title."""
        for period in Const.month_cell_periods():
            self.ws.merge_cells(period)

    def set_month_title(self):
        """Defines the month titles."""
        for index, coord in enumerate(Const.month_cell_periods_start()):
            self.ws[f'{coord}'].value = self.cells_month[index]
            self.ws[f'{coord}']._style = self.set_style_cell(coord=coord, style_name=ConstDefault.dict_month_title_styles[index].name)

    def set_default(self):
        """Applies the basic style for the whole table."""
        for row in rows_from_range(f'A1:NT18'):
            for coord in row:
                cell: Cell = self.ws[f'{coord}']
                cell._style = self.set_style_cell(coord=coord, style_name='basic')

    def set_weekends(self):
        """Applies the weekend style."""
        for column_letter in self.cols_weekend:
            for row in self.rows_weekend:
                coord = f'{column_letter}{row}'
                cell: Cell = self.ws[f'{coord}']
                cell._style = self.set_style_cell(coord=coord, style_name='weekend')

    def set_headers(self):
        """Applies the headers."""
        for row, value in self.cells_headers:
            # merge the cells
            self.ws.merge_cells(f'B{row}:E{row}')

            cell: Cell = self.ws[f'B{row}']
            cell.value = value
            cell._style = self.set_style_cell(coord=cell.coordinate, style_name='headers')

    def set_headers_row(self):
        """Applies the headers row."""
        for row, value in self.cells_headers:
            cell_range: tuple[Cell] = self.ws[f'F{row}:NT{row}']
            row_range: tuple[Cell]
            cell: Cell
            for row_range in cell_range:
                for cell in row_range:
                    cell._style = self.set_style_cell(coord=cell.coordinate, style_name='headers')

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

        for index, style_name in enumerate(Const.dict_legend):
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
                cell._style = self.set_style_cell(coord=cell.coordinate, style_name='table')
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


def save_workbook(wb: Workbook, const: Const, filename: str):
    """
    Save the workbook to the file.\n
    :param wb: the workbook, Workbook
    :param const: the Const entity, Const
    :param filename: the name of file to save, str
    """
    named_style_list = const.named_style_list
    wb._named_styles = named_style_list
    wb.save(filename=filename)


def set_workbook():
    wb = Workbook()
    wb.create_sheet(title='Итог', index=0)
    wb.create_sheet(title='12 мес.', index=1)
    const = Const()
    ws: Worksheet = wb['12 мес.']
    ws_default = WorksheetDefault(wb=wb, ws=ws, const=const)
    # set default
    ws_default.set_default()
    print('ws_default.set_default()')
    # set dates
    ws_default.set_dates()
    print('ws_default.set_dates()')
    # set month titles
    ws_default.set_month_title()
    print('ws_default.set_month_title()')
    # set month headers
    ws_default.set_headers()
    print('ws_default.set_headers()')
    # set headers row
    ws_default.set_headers_row()
    print('ws_default.set_headers_row()')
    # set table
    ws_default.set_table()
    print('ws_default.set_table()')
    # set weekend
    ws_default.set_weekends()
    print('ws_default.set_weekends()')
    # set legend
    ws_default.set_legend()
    print('ws_default.set_legend()')

    named_style_list = [*const.named_style_list]
    # style_array = [named_style.as_tuple() for named_style in named_style_list]
    wb._named_styles = []
    for named_style in named_style_list:
        if named_style not in wb._named_styles:
            wb.add_named_style(named_style)
    # wb._named_styles = named_style_list
    wb.save('test_xlsx.xlsx')


def main():
    set_workbook()


if __name__ == '__main__':
    main()
