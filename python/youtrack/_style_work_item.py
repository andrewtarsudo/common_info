from copy import copy
from typing import Optional, Union

from openpyxl.styles.numbers import FORMAT_GENERAL, FORMAT_TEXT, FORMAT_NUMBER_00, FORMAT_DATE_XLSX14
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.borders import Border, Side, BORDER_THIN, BORDER_THICK
from openpyxl.styles.colors import Color, WHITE, BLACK
from openpyxl.styles.fills import PatternFill, FILL_SOLID
from openpyxl.styles.fonts import Font
from openpyxl.styles.protection import Protection
from openpyxl.cell.cell import Cell
from openpyxl.styles.named_styles import NamedStyle


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
        THICK_BORDER --- True, Side(style=BORDER_THICK)\n
        TOP_BOTTOM_BORDER --- True, Side(style=BORDER_THIN),
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
        "verified_closed", "going_finish", "sick", "vacation"
    dict_months_color --- dict of months, PatternFill values
        "january", "february", "march", "april", "may", "june",\n
        "july", "august", "september", "october", "november", "december"
    """
    # Cell.alignment
    TMP_ALIGNMENT = Alignment(horizontal='left', vertical='center', wrap_text=True)
    CENTER_ALIGNMENT = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ROTATE_ALIGNMENT = Alignment(horizontal='center', vertical='center', wrap_text=True, text_rotation=90)
    # Cell.border
    TMP_BORDER = Border(outline=False, left=Side(), right=Side(), top=Side(), bottom=Side(), diagonal=Side())
    THIN_BORDER = Border(
        outline=True, left=Side(style=BORDER_THIN), right=Side(style=BORDER_THIN), top=Side(style=BORDER_THIN),
        bottom=Side(style=BORDER_THIN))
    THICK_BORDER = Border(
        outline=True, left=Side(style=BORDER_THICK), right=Side(style=BORDER_THICK), top=Side(style=BORDER_THICK),
        bottom=Side(style=BORDER_THICK))
    TOP_BOTTOM_BORDER = Border(
        outline=True, left=Side(style=BORDER_THIN), right=Side(style=BORDER_THIN), top=Side(style=BORDER_THICK),
        bottom=Side(style=BORDER_THICK))
    # Cell.fill
    TMP_FILL = PatternFill(
        fill_type=FILL_SOLID, fgColor=Color(rgb=WHITE, type='rgb'), bgColor=Color(rgb=WHITE, type='rgb'))
    INDEXED_FILL = PatternFill(
        fill_type=FILL_SOLID, fgColor=Color(rgb=WHITE, type='rgb'), bgColor=Color(indexed=64, type='indexed'))
    TINT_FILL = PatternFill(
        fill_type=FILL_SOLID, fgColor=Color(theme=0, tint=0.0, type='theme'), bgColor=Color(indexed=64, type='indexed'))
    # Cell.font
    TMP_FONT = Font(name='Calibri', charset=204, family=2, color=Color(rgb=BLACK, type='rgb'), size=11)
    THEME_FONT = Font(name='Calibri', charset=204, family=2, color=Color(theme=1, type='theme'), size=11)
    # Cell.protection
    TMP_PROTECTION = Protection(locked=False, hidden=False)
    # states and PatternFill values
    dict_states_color: dict[str, PatternFill] = {
        "weekend": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFFD5635", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "deadline": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFFF0D0D", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "done": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=9, tint=0.0, type='theme'),
            bgColor=Color(indexed=64, type='indexed')),
        "active": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=9, tint=0.3999755851924192, type='theme'),
            bgColor=Color(indexed=64, type='indexed')),
        "test": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF117D68", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "going_start": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF00B0F0", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "paused": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=0, tint=-0.499984740745262, type='theme'),
            bgColor=Color(indexed=64, type='indexed')),
        "verified_closed": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=1, tint=0.249977111117893, type='theme'),
            bgColor=Color(indexed=64, type='indexed')),
        "going_finish": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=4, tint=-0.249977111117893, type='theme'),
            bgColor=Color(indexed=64, type='indexed')),
        "sick": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=7, tint=-0.249977111117893, type='theme'),
            bgColor=Color(indexed=64, type='indexed')),
        "vacation": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFFFFF00", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb'))
    }
    # months and PatternFill values
    dict_months_color = {
        "january": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF0297CC", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "february": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF0BA6B6", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "march": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF3AAA66", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "april": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF8BBD36", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "may": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFD0CA04", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "june": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFF9AD01", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "july": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFF08002", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "august": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFE94442", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "september": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FFCF687D", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "october": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF98668B", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "november": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF697FB9", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb')),
        "december": PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(rgb="FF0078A9", type='rgb'), bgColor=Color(rgb=WHITE, type='rgb'))
    }
    # dict of _StyleWorkItems
    dict_style_work_item = dict()


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
        _get_named -> _StyleWorkItem --- convert to the NamedStyle instance;

    Functions:
        get_style_cell(name, cell) -> _StyleWorkItem --- get the cell style;\n
        basic() -> _StyleWorkItem --- set the basic style;\n
        basic_state_style() -> _StyleWorkItem --- set the basic state style;\n
        state_styles() -> list[_StyleWorkItem] --- set the state styles;\n
        basic_month_style() -> _StyleWorkItem --- set the basic month style;\n
        month_styles() -> list[_StyleWorkItem] --- set the basic month styles;\n
        month_merged_styles() -> list[_StyleWorkItem] --- set the merged month styles;\n
        title() -> _StyleWorkItem --- set the title style;\n
        header() -> _StyleWorkItem --- set the header style;\n
        month_date_style() -> _StyleWorkItem --- set the month date style;\n
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

        ConstStyle.dict_style_work_item[self.name] = self

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

    def __getattribute__(self, key):
        if key in _StyleWorkItem.list_attrs:
            return object.__getattribute__(self, key)
        else:
            print(f"AttributeError, the attribute {key} is not specified.")
            return None

    def __setattr__(self, key, value):
        if key in _StyleWorkItem.list_attrs:
            object.__setattr__(self, key, value)

    @staticmethod
    def get_style_cell(name: str, cell: Cell):
        """
        Get the style of the cell.

        :param str name: the style name
        :param Cell cell: the cell to get the style
        :return: the _StyleWorkItem instance.
        :rtype: _StyleWorkItem or None
        """
        if cell.has_style:
            return _StyleWorkItem(
                name, number_format=cell.number_format, alignment=cell.alignment, border=cell.border, fill=cell.fill,
                font=cell.font, protection=cell.protection, data_type=cell.data_type)
        else:
            return None

    @property
    def _get_named(self):
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

    @staticmethod
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

    @staticmethod
    def basic_state_style():
        """
        Specify the basic state style.

        :return: the basic style for states.
        :rtype: _StyleWorkItem
        """
        return _StyleWorkItem(
            "basic_style", False, number_format=FORMAT_NUMBER_00, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.THIN_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="n")

    @staticmethod
    def state_styles():
        """
        Specify the state styles.

        :return: the state styles.
        :rtype: list[_StyleWorkItem]
        """
        return [generate_from_style(name, _StyleWorkItem.basic_state_style(), ["_is_named", "fill"], [True, fill])
                for name, fill in ConstStyle.dict_states_color.items()]

    @staticmethod
    def basic_month_style():
        """
        Specify the basic month style.

        :return: the basic style for months.
        :rtype: _StyleWorkItem
        """
        return _StyleWorkItem(
            "basic_month", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.THICK_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="s")

    @staticmethod
    def month_styles():
        """
        Specify the month title styles.

        :return: the styles for month titles.
        :rtype: list[_StyleWorkItem]
        """
        return [generate_from_style(
                month, _StyleWorkItem.basic_month_style(), ["alignment", "fill"], [ConstStyle.ROTATE_ALIGNMENT, fill])
                for month, fill in ConstStyle.dict_months_color.items()]

    @staticmethod
    def month_merged_styles():
        """
        Specify the month styles for merged cells.

        :return: the styles for merged month titles.
        :rtype: list[_StyleWorkItem]
        """
        return [generate_from_style(month, _StyleWorkItem.basic_month_style(), ["fill"], [fill])
                for month, fill in ConstStyle.dict_months_color.items()]

    @staticmethod
    def title():
        """
        Specify the title style.

        :return: the title style.
        :rtype: _StyleWorkItem
        """
        title_fill = PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=4, tint=-0.249977111117893, type='theme'),
            bgColor=Color(indexed=64, type='indexed'))
        return _StyleWorkItem(
            "title", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.TOP_BOTTOM_BORDER, fill=title_fill, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="s")

    @staticmethod
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
            "header", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.TOP_BOTTOM_BORDER, fill=header_fill, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="s")

    @staticmethod
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
    if check_attrs and check_values and check_length:
        return _StyleWorkItem.basic()
    else:
        style = copy(base_style)
        style.name = name
        for attr, value in zip(attrs, values):
            setattr(style, attr, value)
        return style


class _StyleWorkItemList:
    """
    Define the style list.
    
    Constants:
        list_states --- the states:
            "weekend", "deadline", "done",\n
            "active", "test", "going_start",\n
            "paused", "verified_closed",\n
            "going_finish", "sick",\n
            "vacation"
    
    Properties:
        style_names -> list[str] --- get the style names;\n
        _get_styles -> list[Union[NamedStyle, _StyleWorkItem]] --- get the styles;
    
    Functions:
        get_style(style_name) -> _StyleWorkItem --- get the style by name;\n
        set_list(name, style_names) --- set the style list;
    """
    list_states = (
        "weekend", "deadline", "done", "active", "test", "going_start", "paused",
        "verified_closed", "going_finish", "sick", "vacation")

    __slots__ = ("name", "styles")

    def __init__(self, 
                 name: str, 
                 styles: list[_StyleWorkItem] = None):
        
        if styles is None:
            styles = []
        
        self.name = name
        self.styles = styles
    
    def __str__(self):
        str_styles = [style.name for style in self.styles]
        unified_str_styles = ", ".join(str_styles)
        return f"_StyleWorkItemList: name = {self.name}, styles: {unified_str_styles}"
    
    def __repr__(self):
        repr_styles = [repr(style) for style in self.styles]
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

    def __contains__(self, item):
        return item in self.styles

    def __getitem__(self, item):
        return self.styles[item]

    def __setitem__(self, key, value):
        self.styles[key] = value

    def __iter__(self):
        return (item for item in self.styles)

    def get_style(self, style_name: str) -> _StyleWorkItem:
        """
        Get the style from the list by name.
        
        :param str style_name: the style name
        :return: the style.
        :rtype: _StyleWorkItem
        """
        if style_name == "basic":
            return _StyleWorkItem.basic()
        elif style_name in _StyleWorkItemList.list_states:
            for style in self.styles:
                if style.name == style_name:
                    return style

    @property
    def style_names(self) -> list[str]:
        """
        Get the style names.
        
        :return: the names of the styles.
        :rtype: list[str]
        """
        return [style.name for style in self.styles]

    @property
    def _get_styles(self) -> list[Union[NamedStyle, _StyleWorkItem]]:
        """
        Get all styles in the list.
        
        :return: the styles.
        :rtype: list[NamedStyle and _StyleWorkItem] 
        """
        style: _StyleWorkItem
        for name, style in ConstStyle.dict_style_work_item.items():
            if name not in self.style_names:
                self.styles.append(style._get_named)
        return self.styles

    @classmethod
    def set_list(cls, name: str, style_names: list[str] = None):
        """
        Define the style list.
        
        :param str name: the list name 
        :param style_names: the names of the styles
        :type: list[str] or None
        :return: the style list.
        :rtype: _StyleWorkItemList
        """
        if style_names is not None:
            styles = [ConstStyle.dict_style_work_item[style_name] for style_name in style_names]
        else:
            styles = []
        return cls(name, styles)


def main():
    pass


if __name__ == "__main__":
    main()
