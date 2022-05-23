from typing import Optional
import openpyxl
from openpyxl.cell.cell import Cell
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from yt_config import UserConfig
from yt_requests import User, Issue, IssueWorkItem, _IssueMerged
from xl_table import ExcelProp, PyXLRow, PyXLWorkItem, _PyXLMerged
from _style_work_item import _StyleWorkItemList
import datetime


def separate_issues(excel_prop: ExcelProp, user: User) -> dict[str, list[str]]:
    """
    Separate issues depending on the following actions with them.

    :param excel_prop: the ExcelProp instance
    :param user: the User instance
    :return: the dictionary of states and issue names.
    :rtype: dict[str, list[str]]
    """
    dict_issue_names: dict[str, list[str]] = dict()
    # issue names
    xl_names = set(excel_prop.pyxl_row_names())
    yt_names = set(user.issue_names())
    # issues from the tables left unchanged
    dict_issue_names["xl_names_not_changed"] = [*xl_names.difference(yt_names)]
    # issues from the YouTrack to add to the table
    dict_issue_names["yt_names_add"] = [*yt_names.difference(xl_names)]
    # issues that changed
    dict_issue_names["names_changed"] = [*set.intersection(xl_names, yt_names)]
    return dict_issue_names


def _convert_to_pyxl_row(issue_merged: _IssueMerged, excel_prop: ExcelProp) -> PyXLRow:
    """
    Generate the task in the table.

    :param _IssueMerged issue_merged: the _IssueMerged instance
    :param ExcelProp excel_prop: the ExcelProp instance
    :return: the new task.
    :rtype: PyXLRow
    """
    issue, state, summary, parent, deadline = issue_merged.issue_item.to_tuple()
    # get the new row
    row: int = excel_prop.add_row(state)
    # add the row
    excel_prop.ws.insert_rows(row)
    # parse the values to the new table row
    excel_prop.ws[f"B{row}"].value = parent
    excel_prop.ws[f"C{row}"].value = issue
    excel_prop.ws[f"D{row}"].value = summary
    excel_prop.ws[f"E{row}"].value = deadline
    # set the base cell
    cell: Cell = excel_prop.ws[f"C{row}"]
    return PyXLRow(excel_prop, cell)


def _convert_to_pyxl_work_items(issue_merged: _IssueMerged, excel_prop: ExcelProp) -> list[PyXLWorkItem]:
    """
    Generate the work items in the table.

    :param _IssueMerged issue_merged: the _IssueMerged instance
    :param ExcelProp excel_prop: the ExcelProp instance
    :return: the new work items.
    :rtype: list[PyXLWorkItem]
    """
    work_items = []
    for work_item in issue_merged.work_items:
        date: datetime.date = work_item.date
        column: str = excel_prop.get_column_date(date)
        row: int = excel_prop.add_row(issue_merged.issue_item.state)
        cell: Cell = excel_prop.ws[f"{column}{row}"]
        work_items.append(PyXLWorkItem(excel_prop, cell))
    return work_items


def convert_to_xl_merged(issue_merged: _IssueMerged, excel_prop: ExcelProp):
    """
    Generate the _PyXLMerged in the table.

    :param _IssueMerged issue_merged: the _IssueMerged instance
    :param ExcelProp excel_prop: the ExcelProp instance
    :return: None.
    """
    work_items = _convert_to_pyxl_work_items(issue_merged, excel_prop)
    pyxl_row = _convert_to_pyxl_row(issue_merged, excel_prop)
    cell = pyxl_row.issue
    pyxl_merged = _PyXLMerged(excel_prop, cell)
    for work_item in work_items:
        work_item.set_style()


def compare_merged_issue(issue_merged: _IssueMerged, pyxl_merged: _PyXLMerged) -> Optional[Issue]:
    """
    Get the unequal issue if any.

    :param _IssueMerged issue_merged: the instances from the YouTrack
    :param _PyXLMerged pyxl_merged: the instances from the table
    :return: the instances from the YouTrack to add or modify in the table.
    :rtype: None or Issue
    """
    return None if issue_merged.issue_item.to_tuple() == pyxl_merged.pyxl_row.to_tuple() else issue_merged.issue_item


def compare_merged_work_item(issue_merged: _IssueMerged, pyxl_merged: _PyXLMerged) -> Optional[list[IssueWorkItem]]:
    """
    Get the unequal work items if any.

    :param _IssueMerged issue_merged: the instances from the YouTrack
    :param _PyXLMerged pyxl_merged: the instances from the table
    :return: the instances from the YouTrack to add or modify in the table.
    :rtype: None or list[IssueWorkItem]
    """
    # issue, date, spent_time
    return [work_item for work_item in issue_merged.work_items
            if work_item.to_tuple() not in pyxl_merged.items_to_tuple()]


def get_modified_attr_pyxl_row(issue_merged: _IssueMerged, pyxl_merged: _PyXLMerged) -> list[tuple]:
    """
    Get the PyXLRow attributes and values to modify.

    :param _IssueMerged issue_merged: the instances from the YouTrack
    :param _PyXLMerged pyxl_merged: the instances from the table
    :return: the parameters to modify.
    :rtype: list[tuple[str, Any]]
    """
    attrs = "state", "summary", "parent", "deadline"
    return [(attr, getattr(issue_merged, attr)) for attr in attrs
            if getattr(issue_merged, attr) != getattr(pyxl_merged, attr)]


def merge_issues(issue_name: str, user: User, excel_prop: ExcelProp) -> tuple[_IssueMerged, _PyXLMerged]:
    return user.dict_issue_merged[issue_name], excel_prop.dict_pyxl_merged[issue_name]


def modify_issues():
    pass


def main():
    youtrack_config = UserConfig()
    user = User(youtrack_config)
    user.get_issue_work_items()
    user.get_issues()
    user.get_current_issues()
    yt_issues_merged = user.get_merged()

    path = youtrack_config.get_json_attr("path_table")
    wb = openpyxl.load_workbook(path)
    ws: Worksheet = wb["12 мес."]
    style_list = _StyleWorkItemList("styles")
    excel_prop = ExcelProp(ws, "excel_prop", style_list)
    pyxl_issues_merged = excel_prop.get_merged()

    dict_issues = separate_issues(excel_prop, user)

    for issue_name in dict_issues["yt_names_add"]:
        yt_issue_merged = user.dict_issue_merged[issue_name]
        convert_to_xl_merged(yt_issue_merged, excel_prop)

    issue_modified = []
    work_item_modified = []

    for issue_name in dict_issues["names_changed"]:
        yt_issue_merged, pyxl_issue_merged = merge_issues(issue_name, user, excel_prop)

        issue_compared = compare_merged_issue(yt_issue_merged, pyxl_issue_merged)
        if issue_compared is not None:
            issue_modified.append(issue_compared.issue)

        work_item_compared = compare_merged_work_item(yt_issue_merged, pyxl_issue_merged)
        if work_item_compared is not None:
            for item in work_item_compared:
                work_item_modified.append(item)

    for issue_name in issue_modified:
        yt_issue_merged, pyxl_issue_merged = merge_issues(issue_name, user, excel_prop)
        attrs = get_modified_attr_pyxl_row(yt_issue_merged, pyxl_issue_merged)
        for attr, attr_value in attrs:
            if attr == "state":
                pyxl_issue_merged.modify_pyxl_state(attr_value)
            else:
                column = excel_prop.dict_attr_column[attr]
                row = pyxl_issue_merged.row
                excel_prop.ws[f"{column}{row}"].value = attr_value

    for work_item in work_item_modified:
        excel_prop.add_work_item(work_item.issue, work_item.date, work_item.spent_time)
    print("The work is finished.")
    wb.save(f"copy_{user.path_table}")


if __name__ == "__main__":
    main()
