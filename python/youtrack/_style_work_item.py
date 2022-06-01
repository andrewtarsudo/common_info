"""
basic() -> _StyleWorkItem --- set the basic style;\n
basic_state_style() -> _StyleWorkItem --- set the basic state style;\n
state_styles() -> list[_StyleWorkItem] --- set the state styles;\n
basic_month_style() -> _StyleWorkItem --- set the basic month style;\n
month_styles() -> list[_StyleWorkItem] --- set the basic month styles;\n
month_merged_styles() -> list[_StyleWorkItem] --- set the merged month styles;\n
title() -> _StyleWorkItem --- set the title style;\n
header() -> _StyleWorkItem --- set the header style;\n
month_date_style() -> _StyleWorkItem --- set the month date style;
generate_from_style(name, base_style, cell_attrs, values) -> _StyleWorkItem --- set the style based on the other one;
"""

from copy import copy
from typing import Union
from openpyxl.styles.numbers import FORMAT_GENERAL, FORMAT_TEXT, FORMAT_NUMBER_00, FORMAT_DATE_XLSX14
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.borders import Border, Side, BORDER_THIN, BORDER_THICK, BORDER_MEDIUM
from openpyxl.styles.colors import Color, WHITE, BLACK
from openpyxl.styles.fills import PatternFill, FILL_SOLID
from openpyxl.styles.fonts import Font
from openpyxl.styles.protection import Protection
from openpyxl.cell.cell import Cell
from openpyxl.styles.named_styles import NamedStyle
from openpyxl.workbook.workbook import Workbook


def basic():
    """
    Specify the basic style.

    :return: the basic style.
    :rtype: _StyleWorkItem
    """
    return _StyleWorkItem(
        "basic", True, number_format=FORMAT_GENERAL, alignment=ConstStyle.TMP_ALIGNMENT,
        border=ConstStyle.TMP_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.TMP_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="s"
    )


def _basic_state_style():
    """
    Specify the basic state style.

    :return: the basic style for states.
    :rtype: _StyleWorkItem
    """
    return _StyleWorkItem(
        "_basic_style", False, number_format=FORMAT_NUMBER_00, alignment=ConstStyle.CENTER_ALIGNMENT,
        border=ConstStyle.THIN_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.THEME_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="n")


def state_styles():
    """
    Specify the state styles.

    :return: the state styles.
    :rtype: list[_StyleWorkItem]
    """
    return [generate_from_style(name, _basic_state_style(), ["_is_named", "fill"], [True, fill])
            for name, fill in ConstStyle.dict_states_color.items()]


def _basic_month_style():
    """
    Specify the basic month style.

    :return: the basic style for months.
    :rtype: _StyleWorkItem
    """
    return _StyleWorkItem(
        "_basic_month", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
        border=ConstStyle.MEDIUM_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.THEME_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="s")


def month_styles():
    """
    Specify the month title styles.

    :return: the styles for month titles.
    :rtype: list[_StyleWorkItem]
    """
    return [generate_from_style(
        f"{month}_header", _basic_month_style(), ["alignment", "fill"], [ConstStyle.ROTATE_ALIGNMENT, fill])
        for month, fill in ConstStyle.dict_months_color.items()]


def month_merged_styles():
    """
    Specify the month styles for merged cells.

    :return: the styles for merged month titles.
    :rtype: list[_StyleWorkItem]
    """
    return [generate_from_style(f"{month}_title", _basic_month_style(), ["fill"], [fill])
            for month, fill in ConstStyle.dict_months_color.items()]


def title():
    """
    Specify the title style.

    :return: the title style.
    :rtype: _StyleWorkItem
    """
    title_fill = PatternFill(
        fill_type=FILL_SOLID, fgColor=Color(theme=3, tint=0.7999816888943144, type='theme'),
        bgColor=Color(indexed=64, type='indexed'))
    return _StyleWorkItem(
        "title", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
        border=ConstStyle.TOP_BOTTOM_MEDIUM_BORDER, fill=title_fill, font=ConstStyle.THEME_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="s")


def header():
    """
    Specify the header style.

    :return: the header style.
    :rtype: _StyleWorkItem
    """
    header_fill = PatternFill(
        fill_type=FILL_SOLID, fgColor=Color(theme=3, tint=0.5999938962981048, type='theme'),
        bgColor=Color(indexed=64, type='indexed'))
    return _StyleWorkItem(
        "header", True, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
        border=ConstStyle.TOP_BOTTOM_MEDIUM_BORDER, fill=header_fill, font=ConstStyle.THEME_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="s")


def month_date_style():
    """
    Specify the month date style.

    :return: the month date style.
    :rtype: _StyleWorkItem
    """
    return _StyleWorkItem(
        "month_date", False, number_format=FORMAT_DATE_XLSX14, alignment=ConstStyle.CENTER_ALIGNMENT,
        border=ConstStyle.TMP_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.TMP_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="d"
    )


def deadline_issue_style():
    # TODO
    """
    Specify the issue deadline style.

    :return: the issue deadline style.
    :rtype: _StyleWorkItem
    """
    return _StyleWorkItem(
        "deadline_issue", False, number_format=FORMAT_DATE_XLSX14, alignment=ConstStyle.TMP_ALIGNMENT,
        border=ConstStyle.LEFT_RIGHT_MEDIUM_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.THEME_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="d"
    )


def header_cross_style():
    # TODO
    """
    Specify the header cross style.

    :return: the header cross style.
    :rtype: _StyleWorkItem
    """
    header_cross_fill = PatternFill(
        fill_type=FILL_SOLID, fgColor=Color(theme=3, tint=0.5999938962981048, type='theme'),
        bgColor=Color(indexed=64, type='indexed'))
    return _StyleWorkItem(
        "header_cross", False, number_format=FORMAT_GENERAL, alignment=ConstStyle.NONE_ALIGNMENT,
        border=ConstStyle.TMP_BORDER, fill=header_cross_fill, font=ConstStyle.THEME_FONT,
        protection=ConstStyle.TMP_PROTECTION, data_type="s"
    )


class ConstStyle:
    """
    Contain the constants for Named and Cell Styles.

    Alignment(horizontal, vertical, wrap_text):
        TMP_ALIGNMENT --- left, center, True\n
        CENTER_ALIGNMENT --- center, center, True\n
        ROTATE_ALIGNMENT --- center, center, True, 90\n

    Border(outline, left, right, top, bottom, diagonal):
        TMP_BORDER --- False, Side(), Side(), Side(), Side(), Side()\n
        THIN_BORDER --- True, Side(style=BORDER_THIN)\n
        MEDIUM_BORDER --- True, Side(style=BORDER_THICK)\n
        TOP_BOTTOM_MEDIUM_BORDER --- True, Side(style=BORDER_THIN),
            Side(BORDER_THICK)\n

    PatternFill(fill_type, fgColor, bgColor):
        TMP_FILL --- FILL_SOLID, Color(rgb=WHITE, type='rgb'),
            Color(rgb=WHITE, type='rgb')\n
        INDEXED_FILL --- FILL_SOLID, Color(rgb=WHITE, type='rgb'),
            Color(indexed=64, type='indexed')\n
        TINT_FILL --- FILL_SOLID, Color(theme=0, tint=0.0, type='theme'),
            Color(indexed=64, type='indexed')\n

    Font(name, charset, family, color, size):
        TMP_FONT --- 'Calibri', 204, 2, Color(rgb=BLACK, type='rgb'), 11\n
        THEME_FONT --- 'Calibri', 204, 2, Color(theme=1, type='theme'), 11\n

    Protection(locked, hidden):
        TMP_PROTECTION --- False, False\n

    dict_states_color --- dict of states, PatternFill values
        "weekend", "deadline", "done", "active", "test", "going_start", "paused",
        "verified_closed", "going_finish", "sick", "vacation"\n
    dict_months_color --- dict of months, PatternFill values
        "january", "february", "march", "april", "may", "june",\n
        "july", "august", "september", "october", "november", "december"\n
    """
    # Cell.alignment
    TMP_ALIGNMENT = Alignment(
        horizontal='left', vertical='center', wrap_text=True, shrinkToFit=None, indent=0, relativeIndent=0,
        justifyLastLine=None, readingOrder=0)
    CENTER_ALIGNMENT = Alignment(
        horizontal='center', vertical='center', wrap_text=True, shrinkToFit=None, indent=0, relativeIndent=0,
        justifyLastLine=None, readingOrder=0)
    ROTATE_ALIGNMENT = Alignment(
        horizontal='center', vertical='center', wrap_text=True, text_rotation=90, indent=0, relativeIndent=0,
        justifyLastLine=None, readingOrder=0)
    NONE_ALIGNMENT = Alignment()
    # Cell.border
    TMP_BORDER = Border(outline=False,
                        left=Side(style=None, color=None),
                        right=Side(style=None, color=None),
                        top=Side(style=None, color=None),
                        bottom=Side(style=None, color=None),
                        diagonal=Side(style=None, color=None))
    THIN_BORDER = Border(outline=True,
                         left=Side(style=BORDER_THIN, color=Color(rgb=BLACK, type="rgb")),
                         right=Side(style=BORDER_THIN, color=Color(rgb=BLACK, type="rgb")),
                         top=Side(style=BORDER_THIN, color=Color(rgb=BLACK, type="rgb")),
                         bottom=Side(style=BORDER_THIN, color=Color(rgb=BLACK, type="rgb")),
                         diagonal=Side(style=None, color=None))
    MEDIUM_BORDER = Border(outline=True,
                           left=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                           right=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                           top=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                           bottom=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                           diagonal=Side(style=None, color=None))
    TOP_BOTTOM_MEDIUM_BORDER = Border(outline=True,
                                      left=Side(style=None, color=None),
                                      right=Side(style=None, color=None),
                                      top=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                                      bottom=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                                      diagonal=Side(style=None, color=None))
    LEFT_RIGHT_MEDIUM_BORDER = Border(outline=True,
                                      left=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                                      right=Side(style=BORDER_MEDIUM, color=Color(rgb=BLACK, type="rgb")),
                                      top=Side(style=None, color=None),
                                      bottom=Side(style=None, color=None),
                                      diagonal=Side(style=None, color=None))
    # Cell.fill
    TMP_FILL = PatternFill(fill_type=None,
                           fgColor=Color(rgb=WHITE, type='rgb'),
                           bgColor=Color(rgb=WHITE, type='rgb'))
    INDEXED_FILL = PatternFill(fill_type=FILL_SOLID,
                               fgColor=Color(rgb=WHITE, type='rgb'),
                               bgColor=Color(indexed=64, type='indexed'))
    TINT_FILL = PatternFill(fill_type=FILL_SOLID,
                            fgColor=Color(theme=0, tint=0.0, type='theme'),
                            bgColor=Color(indexed=64, type='indexed'))
    # Cell.font
    TMP_FONT = Font(name='Times New Roman', charset=204, family=1, color=Color(rgb=BLACK, type='rgb'), size=11)
    THEME_FONT = Font(name='Calibri', charset=204, family=2, color=Color(theme=1, type='theme'), size=11)
    TITLE_FONT = Font(name='Calibri', charset=204, family=2, bold=True, color=Color(theme=1, type='theme'), size=11)
    # Cell.protection
    TMP_PROTECTION = Protection(locked=False, hidden=False)
    # states and PatternFill values
    dict_states_color: dict[str, PatternFill] = {
        "weekend": PatternFill(fill_type=FILL_SOLID,
                               fgColor=Color(rgb="FFFD5635", type='rgb'),
                               bgColor=Color(rgb=WHITE, type='rgb')),
        "deadline": PatternFill(fill_type=FILL_SOLID,
                                fgColor=Color(rgb="FFFF0D0D", type='rgb'),
                                bgColor=Color(rgb=WHITE, type='rgb')),
        "done": PatternFill(fill_type=FILL_SOLID,
                            fgColor=Color(theme=9, tint=0.0, type='theme'),
                            bgColor=Color(indexed=64, type='indexed')),
        "active": PatternFill(fill_type=FILL_SOLID,
                              fgColor=Color(theme=9, tint=0.3999755851924192, type='theme'),
                              bgColor=Color(indexed=64, type='indexed')),
        "test": PatternFill(fill_type=FILL_SOLID,
                            fgColor=Color(rgb="FF117D68", type='rgb'),
                            bgColor=Color(rgb=WHITE, type='rgb')),
        "going_start": PatternFill(fill_type=FILL_SOLID,
                                   fgColor=Color(rgb="FF00B0F0", type='rgb'),
                                   bgColor=Color(rgb=WHITE, type='rgb')),
        "paused": PatternFill(fill_type=FILL_SOLID,
                              fgColor=Color(theme=0, tint=-0.499984740745262, type='theme'),
                              bgColor=Color(indexed=64, type='indexed')),
        "verified_closed": PatternFill(fill_type=FILL_SOLID,
                                       fgColor=Color(theme=1, tint=0.249977111117893, type='theme'),
                                       bgColor=Color(indexed=64, type='indexed')),
        "going_finish": PatternFill(fill_type=FILL_SOLID,
                                    fgColor=Color(theme=4, tint=-0.249977111117893, type='theme'),
                                    bgColor=Color(indexed=64, type='indexed')),
        "sick": PatternFill(fill_type=FILL_SOLID,
                            fgColor=Color(theme=7, tint=-0.249977111117893, type='theme'),
                            bgColor=Color(indexed=64, type='indexed')),
        "vacation": PatternFill(fill_type=FILL_SOLID,
                                fgColor=Color(rgb="FFFFFF00", type='rgb'),
                                bgColor=Color(rgb=WHITE, type='rgb'))
    }
    # months and PatternFill values
    dict_months_color = {
        "january": PatternFill(fill_type=FILL_SOLID,
                               fgColor=Color(rgb="FF0297CC", type='rgb'),
                               bgColor=Color(rgb=WHITE, type='rgb')),
        "february": PatternFill(fill_type=FILL_SOLID,
                                fgColor=Color(rgb="FF0BA6B6", type='rgb'),
                                bgColor=Color(rgb=WHITE, type='rgb')),
        "march": PatternFill(fill_type=FILL_SOLID,
                             fgColor=Color(rgb="FF3AAA66", type='rgb'),
                             bgColor=Color(rgb=WHITE, type='rgb')),
        "april": PatternFill(fill_type=FILL_SOLID,
                             fgColor=Color(rgb="FF8BBD36", type='rgb'),
                             bgColor=Color(rgb=WHITE, type='rgb')),
        "may": PatternFill(fill_type=FILL_SOLID,
                           fgColor=Color(rgb="FFD0CA04", type='rgb'),
                           bgColor=Color(rgb=WHITE, type='rgb')),
        "june": PatternFill(fill_type=FILL_SOLID,
                            fgColor=Color(rgb="FFF9AD01", type='rgb'),
                            bgColor=Color(rgb=WHITE, type='rgb')),
        "july": PatternFill(fill_type=FILL_SOLID,
                            fgColor=Color(rgb="FFF08002", type='rgb'),
                            bgColor=Color(rgb=WHITE, type='rgb')),
        "august": PatternFill(fill_type=FILL_SOLID,
                              fgColor=Color(rgb="FFE94442", type='rgb'),
                              bgColor=Color(rgb=WHITE, type='rgb')),
        "september": PatternFill(fill_type=FILL_SOLID,
                                 fgColor=Color(rgb="FFCF687D", type='rgb'),
                                 bgColor=Color(rgb=WHITE, type='rgb')),
        "october": PatternFill(fill_type=FILL_SOLID,
                               fgColor=Color(rgb="FF98668B", type='rgb'),
                               bgColor=Color(rgb=WHITE, type='rgb')),
        "november": PatternFill(fill_type=FILL_SOLID,
                                fgColor=Color(rgb="FF697FB9", type='rgb'),
                                bgColor=Color(rgb=WHITE, type='rgb')),
        "december": PatternFill(fill_type=FILL_SOLID,
                                fgColor=Color(rgb="FF0078A9", type='rgb'),
                                bgColor=Color(rgb=WHITE, type='rgb'))
    }


class _StyleWorkItem:
    """
    Define the style of the cell.

    Constants:
        list_attrs --- the list of attributes:
            "name", "_is_named", "number_format", "alignment", "border", "fill", "font", "protection", "data_type"

    Params:
        name --- the cell style name, name, str;\n
        _is_named --- the cell named style flag, -, str;\n
        number_format --- the cell number format, fmt;\n
        alignment --- the cell alignment, Alignment;\n
        border --- the cell border, Border;\n
        fill --- the cell fill in, Fill;\n
        font --- the cell font, Font;\n
        protection --- the cell protection, Protection;\n
        data_type --- the cell data type, data_type, str;\n

    Properties:
        get_named --- convert to the NamedStyle instance;\n

    Functions:
        set_style(cell/coord) --- set the style of the cell;\n
    """

    list_attrs: tuple[str] = (
        "name", "_is_named", "number_format", "alignment", "border", "fill", "font", "protection", "data_type"
    )

    def __init__(
            self,
            name: str = None,
            _is_named: bool = False, *,
            number_format: str = None,
            alignment: Alignment = None,
            border: Border = None,
            fill: PatternFill = None,
            font: Font = None,
            protection: Protection = None,
            data_type: str = None):

        if number_format is None:
            number_format = FORMAT_GENERAL
        if alignment is None:
            alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        if border is None:
            border = Border(outline=False, left=Side(), right=Side(), top=Side(), bottom=Side(), diagonal=Side())
        if fill is None:
            fill = PatternFill(fill_type=FILL_SOLID, fgColor=Color(rgb=WHITE, type='rgb'),
                               bgColor=Color(rgb=WHITE, type='rgb'))
        if font is None:
            font = Font(name='Calibri', charset=204, family=2, color=Color(rgb=BLACK, type='rgb'), size=11)
        if protection is None:
            protection = Protection(locked=False, hidden=False)
        if data_type is None:
            data_type = "s"

        self.name = name
        self._is_named = _is_named
        self.number_format = number_format
        self.alignment = alignment
        self.border = border
        self.fill = fill
        self.font = font
        self.protection = protection
        self.data_type = data_type

    def __str__(self):
        return f"name = {self.name}, number_format = {self.number_format}, alignment = {self.alignment}, " \
               f"border = {self.border}, fill = {self.fill}, font = {self.font}, protection = {self.protection}, " \
               f"data_type = {self.data_type}"

    def __repr__(self):
        return f"StyleWorkItem(name={self.name}, number_format={self.number_format}, alignment={self.alignment}, " \
               f"border={self.border}, fill={self.fill}, font={self.font}, protection={self.protection}), " \
               f"data_type={self.data_type}"

    def __hash__(self):
        return hash((self.name, self.number_format, self.alignment, self.border, self.fill,
                     self.font, self.protection, self.data_type))

    def __eq__(self, other):
        if isinstance(other, _StyleWorkItem):
            return self.name == other.name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _StyleWorkItem):
            return self.name != other.name
        else:
            return NotImplemented

    def __bool__(self):
        return any((self.name, self.number_format, self.alignment, self.border, self.fill,
                    self.font, self.protection, self.data_type) is not None)

    @property
    def get_named(self):
        """
        Convert the _StyleWorkItem instance to the NamedStyle one.

        :return: the NamedStyle instance or self.
        :rtype: NamedStyle or _StyleWorkItem
        """
        if self._is_named:
            return NamedStyle(
                name=self.name, font=self.font, fill=self.fill, border=self.border, alignment=self.alignment,
                number_format=self.number_format, protection=self.protection)
        else:
            return self

    def set_style(self, cell: Cell):
        """
        Specify the style of the cell.

        :param cell: the cell or the cell coordinates
        :type cell: Cell
        :return: None.
        """
        # apply the alignment
        cell.alignment = copy(self.alignment)
        # apply the border
        cell.border = copy(self.border)
        # apply the fill
        cell.fill = copy(self.fill)
        # apply the font
        cell.font = copy(self.font)
        # apply the protection
        cell.protection = copy(self.protection)
        # apply the number format
        cell.number_format = copy(self.number_format)


def generate_from_style(name: str, base_style: _StyleWorkItem, attrs: list = None, values: list = None):
    """
    Modify the basic style.

    :param str name: the style name
    :param _StyleWorkItem base_style: the base of the style
    :param list attrs: the attributes to change
    :param list values: the attribute values
    :return: the style.
    :rtype: _StyleWorkItem
    """
    check_attrs: bool = (attrs is not None and all(attr in _StyleWorkItem.list_attrs for attr in attrs))
    check_values: bool = values is not None
    check_length: bool = len(attrs) == len(values)
    if not (check_attrs and check_values and check_length):
        return basic()
    else:
        style = copy(base_style)
        style.name = name
        for attr, value in zip(attrs, values):
            setattr(style, attr, value)
        return style


class _StyleWorkItemList:
    """
    Define the style list.

    Params:
        name --- the list name;\n
        styles --- the dict of the styles,
            dict[style_name, _StyleWorkItem];\n

    Functions:
        set_style(style_name, cell/coord) --- set the style to the cell;\n
    """

    def __init__(self, name: str):
        self.name = name
        self.styles: dict[str, Union[_StyleWorkItem, NamedStyle]] = dict()
        self.styles["basic"] = basic().get_named
        self.styles["_basic_style"] = _basic_state_style().get_named
        self.styles["_basic_month"] = _basic_month_style().get_named
        self.styles["header"] = header().get_named
        self.styles["title"] = title().get_named
        self.styles["month_date"] = month_date_style().get_named
        style: Union[_StyleWorkItem, NamedStyle]
        for style in [*state_styles(), *month_styles(), *month_merged_styles()]:
            self.styles[style.name] = style.get_named

    def __str__(self):
        str_styles = [style_name for style_name in self.styles.keys()]
        unified_str_styles = ", ".join(str_styles)
        return f"_StyleWorkItemList: name = {self.name}, styles: {unified_str_styles}"

    def __repr__(self):
        repr_styles = [repr(style_name) for style_name in self.styles.keys()]
        unified_repr_styles = ",".join(repr_styles)
        return f"_StyleWorkItemList(name={self.name}, styles=[{unified_repr_styles}])"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, _StyleWorkItemList):
            return self.name == other.name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _StyleWorkItemList):
            return self.name != other.name
        else:
            return NotImplemented

    def set_style(self, style_name: str, cell: Cell):
        """
        Specify the style of the cell.

        :param str style_name: the style name
        :param cell: the cell
        :type cell: Cell
        :return: None.
        """
        style = self.styles[style_name]
        if isinstance(style, NamedStyle):
            cell.style = style.name
        elif isinstance(style, _StyleWorkItem):
            style.set_style(cell)
        else:
            print(f"Something went wrong. Cell {cell.coordinate}. Style: {style_name}.")

    def add_styles(self, wb: Workbook):
        """
        Add the named styles to the Workbook styles.

        :param Workbook wb: the Workbook instance
        :return: None.
        """
        wb._named_styles.clear()
        for style_name, style in self.styles.items():
            if not isinstance(style, NamedStyle):
                continue
            else:
                wb._named_styles.append(style)
                style.bind(wb)


def main():
    pass


if __name__ == "__main__":
    main()
