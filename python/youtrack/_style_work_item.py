from copy import copy
from openpyxl.styles.numbers import FORMAT_GENERAL, FORMAT_TEXT, FORMAT_NUMBER_00, FORMAT_DATE_XLSX14
from openpyxl.styles.alignment import Alignment
from openpyxl.styles.borders import Border, Side, BORDER_THIN, BORDER_THICK
from openpyxl.styles.colors import Color, WHITE, BLACK
from openpyxl.styles.fills import PatternFill, FILL_SOLID
from openpyxl.styles.fonts import Font
from openpyxl.styles.protection import Protection
from openpyxl.cell.cell import Cell
from openpyxl.styles.named_styles import NamedStyle


dict_style_work_item = dict()


class ConstStyle:
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


class _StyleWorkItem(object):
    __doc__ = """"""

    list_attrs: tuple[str] = (
        "name", "_is_named", "number_format", "alignment", "border", "fill", "font", "protection", "data_type"
    )

    def __init__(
            self, name: str = None, _is_named: bool = False, *, number_format: str = None, alignment: Alignment = None,
            border: Border = None, fill: PatternFill = None, font: Font = None, protection: Protection = None,
            data_type: str = None):
        """

        :param name:
        :param _is_named:
        :param number_format:
        :param alignment:
        :param border:
        :param fill:
        :param font:
        :param protection:
        :param data_type:
        """
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

        dict_style_work_item[self.name] = self

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

    @classmethod
    def get_style_cell(cls, name: str, cell: Cell):
        """"""
        if cell.has_style:
            return cls(
                name, number_format=cell.number_format, alignment=cell.alignment, border=cell.border, fill=cell.fill,
                font=cell.font, protection=cell.protection, data_type=cell.data_type)
        else:
            return None

    def __getattribute__(self, item):
        if item in self.__class__.list_attrs:
            return object.__getattribute__(self, item)
        else:
            return None

    def __setattr__(self, key, value):
        if key in self.__class__.list_attrs:
            object.__setattr__(self, key, value)

    @property
    def _list_named(self):
        if self._is_named:
            return NamedStyle(
                name=self.name, font=self.font, fill=self.fill, border=self.border, alignment=self.alignment,
                number_format=self.number_format, protection=self.protection)
        else:
            return self

    @staticmethod
    def basic():
        """Specifies the basic style."""
        return _StyleWorkItem(
            "basic", True, number_format=FORMAT_GENERAL, alignment=ConstStyle.TMP_ALIGNMENT,
            border=ConstStyle.TMP_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.TMP_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="s"
        )

    @staticmethod
    def basic_state_style():
        """Specifies the basic state style."""
        return _StyleWorkItem(
            "basic_style", False, number_format=FORMAT_NUMBER_00, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.THIN_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="n")

    @staticmethod
    def state_styles():
        """Specifies the state styles."""
        return [generate_from_style(name, _StyleWorkItem.basic_state_style(), ["_is_named", "fill"], [True, fill])
                for name, fill in ConstStyle.dict_states_color.items()]

    @staticmethod
    def basic_month_style():
        """"""
        return _StyleWorkItem(
            "basic_month", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.THICK_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="s")

    @staticmethod
    def month_styles():
        """Specifies the month title styles."""
        return [generate_from_style(
                month, _StyleWorkItem.basic_month_style(), ["alignment", "fill"], [ConstStyle.ROTATE_ALIGNMENT, fill])
                for month, fill in ConstStyle.dict_months_color.items()]

    @staticmethod
    def month_merged_styles():
        """Specifies the month styles for merged cells."""
        return [generate_from_style(month, _StyleWorkItem.basic_month_style(), ["fill"], [fill])
                for month, fill in ConstStyle.dict_months_color.items()]

    @staticmethod
    def title():
        """Specifies the title style."""
        title_fill = PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=4, tint=-0.249977111117893, type='theme'),
            bgColor=Color(indexed=64, type='indexed'))
        return _StyleWorkItem(
            "title", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.TOP_BOTTOM_BORDER, fill=title_fill, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="s")

    @staticmethod
    def header():
        """Specifies the header style."""
        header_fill = PatternFill(
            fill_type=FILL_SOLID, fgColor=Color(theme=3, tint=0.5999938962981048, type='theme'),
            bgColor=Color(indexed=64, type='indexed'))
        return _StyleWorkItem(
            "header", False, number_format=FORMAT_TEXT, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.TOP_BOTTOM_BORDER, fill=header_fill, font=ConstStyle.THEME_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="s")

    @staticmethod
    def month_date_style():
        """Specifies the month date style."""
        return _StyleWorkItem(
            "month_date", False, number_format=FORMAT_DATE_XLSX14, alignment=ConstStyle.CENTER_ALIGNMENT,
            border=ConstStyle.TMP_BORDER, fill=ConstStyle.TMP_FILL, font=ConstStyle.TMP_FONT,
            protection=ConstStyle.TMP_PROTECTION, data_type="d"
        )


def generate_from_style(name: str, base_style: _StyleWorkItem, attrs: list = None, values: list = None):
    """

    :param name:
    :param base_style:
    :param attrs:
    :param values:
    :return:
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
    __doc__ = """"""
    list_states = (
        "weekend", "deadline", "done", "active", "test", "going_start", "paused",
        "verified_closed", "going_finish", "sick", "vacation")

    __slots__ = ("name", "styles")

    def __init__(self, name: str, styles: list[_StyleWorkItem] = None):
        """

        :param name:
        :param styles:
        """
        super().__init__()
        if styles is None:
            styles = []
        self.name = name
        self.styles = styles

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


    def get_style(self, style_name: str):
        """

        :param style_name:
        :return:
        """
        if style_name == "basic":
            return _StyleWorkItem.basic()
        elif style_name in _StyleWorkItemList.list_states:
            for style in self.styles:
                if style.name == style_name:
                    return self[style]

    @property
    def style_names(self):
        """"""
        return [style.name for style in self.styles]

    @property
    def _get_styles(self):
        style: _StyleWorkItem
        for name, style in dict_style_work_item.items():
            if name not in self.style_names:
                self.styles.append(style._list_named)
        return self.styles

    @classmethod
    def set_list(cls, name: str, style_names: list[str] = None):
        if style_names is not None:
            styles = [dict_style_work_item[style_name] for style_name in style_names]
        else:
            styles = []
        return cls(name, styles)


def main():
    pass


if __name__ == "__main__":
    main()
