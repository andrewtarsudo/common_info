from typing import Optional, Union

import openpyxl
from openpyxl.cell.cell import Cell
from yt_config import UserConfig
from yt_requests import ConstYT, User, Issue, IssueWorkItem, _IssueMerged
from xl_table import ConstXL, ExcelProp, PyXLRow, PyXLWorkItem, _PyXLMerged
from _style_work_item import _StyleWorkItem, _StyleWorkItemList


def compare_merged(
        issue_merged: _IssueMerged, 
        pyxl_merged: _PyXLMerged, 
        instance: str) -> Optional[Union[Issue, set[IssueWorkItem]]]:
    """
    Get the unequal issues and work items if any.
    
    :param _IssueMerged issue_merged: the instances from the YouTrack 
    :param _PyXLMerged pyxl_merged: the instances from the table
    :param instance: the instance type to validate
    :return: the instances from the YouTrack to add or modify in the table.
    :rtype: None or Issue or set[IssueWorkItem]
    """
    issue: Issue = issue_merged.issue_item
    issue_work_items: list[IssueWorkItem] = issue_merged.work_items
    pyxl_row: PyXLRow = pyxl_merged.pyxl_row
    pyxl_items: list[PyXLWorkItem] = pyxl_merged.work_items

    if instance == "issue":
        issue_attrs = issue.issue, issue.state, issue.parent, issue.summary, issue.deadline
        pyxl_row_attrs = pyxl_row.issue, pyxl_row.state, pyxl_row.parent, pyxl_row.summary, pyxl_row.deadline
        if issue_attrs == pyxl_row_attrs:
            return None
        else:
            return issue

    if instance == "items":
        new_work_items = set()
        for work_item in issue_work_items:
            items_attrs = work_item.date, work_item.spent_time
            if any((pyxl_item.date, pyxl_item.spent_time) == items_attrs for pyxl_item in pyxl_items):
                continue
            else:
                new_work_items.add(work_item)
        return new_work_items


def create_pyxl_row(issue: Issue, excel_prop: ExcelProp) -> PyXLRow:
    """
    Create the PyXLRow instance.
    
    :param Issue issue: the Issue instance
    :param ExcelProp excel_prop: the ExcelProp instance
    :return: the PyXLRow instance.
    :rtype: PyXLRow
    """
    state = issue.state
    row = max(excel_prop.list_state_item(state)) + 1
    excel_prop.ws.insert_rows(row)
    excel_prop.ws[f"B{row}"].value = issue.parent
    excel_prop.ws[f"C{row}"].value = issue.issue
    excel_prop.ws[f"D{row}"].value = issue.summary
    excel_prop.ws[f"E{row}"].value = issue.deadline
    return PyXLRow(excel_prop.name, excel_prop.ws[f"C{row}"])


def issue_yt_name(issue_name: str) -> Issue:
    """
    Get the Issue instance by its name.

    :param str issue_name: the issue name
    :return: the Issue instance.
    :rtype: Issue
    """
    issue: Issue
    for issue in ConstYT.dict_issue.values():
        if issue.issue == issue_name:
            return issue
        else:
            continue


def issue_xl_name(issue_name: str) -> PyXLRow:
    """
    Get the PyXLRow instance by its name.

    :param str issue_name: the issue name
    :return: the PyXLRow instance.
    :rtype: PyXLRow
    """
    issue: PyXLRow
    for issue in ConstXL.dict_pyxl_row.values():
        if issue.issue == issue_name:
            return issue
        else:
            continue


def get_row(issue_name: str) -> Optional[int]:
    """
    Specify the row of the issue.

    :param str issue_name: the issue name
    :return: the issue row.
    :rtype: int
    """
    issue: PyXLRow
    if not any(issue.issue == issue_name for issue in ConstXL.dict_pyxl_row.values()):
        return None
    else:
        return issue_xl_name(issue_name).row


def get_row_new_state(excel_prop: ExcelProp, issue_name: str) -> int:
    """
    Specify the row for the new issue.

    :param ExcelProp excel_prop: the ExcelProp instance
    :param str issue_name: the issue name
    :return: the row of the new issue.
    :rtype: int
    """
    state = issue_yt_name(issue_name).state
    row = max(excel_prop.list_state_item(state)) + 1
    return row


def create_pyxl_work_item(issue_work_item: IssueWorkItem, excel_prop: ExcelProp) -> PyXLWorkItem:
    """
    Create the PyXLWorkItem instance.

    :param IssueWorkItem issue_work_item: the IssueWorkItem instance
    :param ExcelProp excel_prop: the ExcelProp instance
    :return: the PyXLWorkItem instance.
    :rtype: PyXLWorkItem
    """
    issue, date, spent_time = issue_work_item.issue, issue_work_item.date, issue_work_item.spent_time
    # the cell column
    column = excel_prop.get_column_date(date)
    # if the issue name is already in the table
    if get_row(issue) is not None:
        row = get_row(issue)
    # if the issue name is not in the table
    else:
        row = get_row_new_state(excel_prop, issue)
        excel_prop.ws.insert_rows(row)
    # define the cell
    cell: Cell = excel_prop.ws[f"{column}{row}"]
    return PyXLWorkItem(excel_prop.name, cell)


def main():
    youtrack_config = UserConfig()
    user = User(youtrack_config)
    user.get_issue_work_items()
    user.get_issues()
    issues_merged = [_IssueMerged(issue_name) for issue_name in ConstYT.dict_issue.keys()]

    path = youtrack_config.get_json_attr("path_table")
    wb = openpyxl.load_workbook(path)

    style_list = _StyleWorkItemList("styles")


if __name__ == "__main__":
    main()
