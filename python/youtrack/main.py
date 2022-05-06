from typing import Optional, Union
import openpyxl
from openpyxl.cell.cell import Cell
from yt_config import UserConfig
from yt_requests import User, Issue, IssueWorkItem, _IssueMerged
from xl_table import ExcelProp, PyXLRow, PyXLWorkItem, _PyXLMerged
from _style_work_item import _StyleWorkItem, _StyleWorkItemList


def compare_merged_issue(issue_merged: _IssueMerged, pyxl_merged: _PyXLMerged):
    """
    Get the unequal issues and work items if any.

    :param _IssueMerged issue_merged: the instances from the YouTrack
    :param _PyXLMerged pyxl_merged: the instances from the table
    :return: the instances from the YouTrack to add or modify in the table.
    :rtype: None or Issue
    """
    issue: Issue = issue_merged.issue_item
    pyxl_row: PyXLRow = pyxl_merged.pyxl_row
    return None if issue.to_tuple() == pyxl_row.to_tuple() else issue


def compare_merged_work_item(issue_merged: _IssueMerged, pyxl_merged: _PyXLMerged):
    """
    Get the unequal issues and work items if any.

    :param _IssueMerged issue_merged: the instances from the YouTrack
    :param _PyXLMerged pyxl_merged: the instances from the table
    :return: the instances from the YouTrack to add or modify in the table.
    :rtype: None or list[IssueWorkItem]
    """
    issue_work_items: list[IssueWorkItem] = issue_merged.work_items
    pyxl_items: list[PyXLWorkItem] = pyxl_merged.work_items
    return [work_unit for work_unit in issue_work_items if
            not any(pyxl_item.to_tuple() == work_unit.to_tuple() for pyxl_item in pyxl_items)]


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
    return PyXLRow(excel_prop, excel_prop.ws[f"C{row}"])


def issue_yt_name(user: User, issue_name: str) -> Issue:
    """
    Get the Issue instance by its name.

    :param User user: the User instance
    :param str issue_name: the issue name
    :return: the Issue instance.
    :rtype: Issue
    """
    issue: Issue
    for issue in user.dict_issue.values():
        if issue.issue == issue_name:
            return issue
        else:
            continue


def issue_xl_name(excel_prop: ExcelProp, issue_name: str) -> PyXLRow:
    """
    Get the PyXLRow instance by its name.

    :param ExcelProp excel_prop: the ExcelProp instance
    :param str issue_name: the issue name
    :return: the PyXLRow instance.
    :rtype: PyXLRow
    """
    issue: PyXLRow
    for issue in excel_prop.dict_pyxl_row.values():
        if issue.issue == issue_name:
            return issue
        else:
            continue


def get_row(excel_prop: ExcelProp, issue_name: str) -> Optional[int]:
    """
    Specify the row of the issue.

    :param ExcelProp excel_prop: the ExcelProp instance
    :param str issue_name: the issue name
    :return: the issue row.
    :rtype: int
    """
    issue: PyXLRow
    if not any(issue.issue == issue_name for issue in excel_prop.dict_pyxl_row.values()):
        return None
    else:
        return issue_xl_name(excel_prop, issue_name).row


def get_row_new_state(user: User, excel_prop: ExcelProp, issue_name: str) -> int:
    """
    Specify the row for the new issue.

    :param User user: the User instance
    :param ExcelProp excel_prop: the ExcelProp instance
    :param str issue_name: the issue name
    :return: the row of the new issue.
    :rtype: int
    """
    state = issue_yt_name(user, issue_name).state
    row = max(excel_prop.list_state_item(state)) + 1
    return row


def create_pyxl_work_item(user: User, issue_work_item: IssueWorkItem, excel_prop: ExcelProp) -> PyXLWorkItem:
    """
    Create the PyXLWorkItem instance.

    :param User user: the User instance
    :param IssueWorkItem issue_work_item: the IssueWorkItem instance
    :param ExcelProp excel_prop: the ExcelProp instance
    :return: the PyXLWorkItem instance.
    :rtype: PyXLWorkItem
    """
    issue, date, spent_time = issue_work_item.issue, issue_work_item.date, issue_work_item.spent_time
    # the cell column
    column = excel_prop.get_column_date(date)
    # if the issue name is already in the table
    if get_row(excel_prop, issue) is not None:
        row = get_row(excel_prop, issue)
    # if the issue name is not in the table
    else:
        row = get_row_new_state(user, excel_prop, issue)
        excel_prop.ws.insert_rows(row)
    # define the cell
    cell: Cell = excel_prop.ws[f"{column}{row}"]
    return PyXLWorkItem(excel_prop, cell, cell.style.name)


def pair_merged(
        issue_merged: list[_IssueMerged],
        pyxl_merged: list[_PyXLMerged]) -> dict[str, tuple[_IssueMerged, _PyXLMerged]]:
    """
    Match the _Merged instances.

    :param issue_merged: the _IssueMerged instances
    :type issue_merged: list[_IssueMerged]
    :param pyxl_merged: the _PyXLMerged instances
    :type issue_merged: list[_PyXLMerged]
    :return: the dictionary of the paired instances.
    """
    yt_pyxl_paired: dict[str, tuple[_IssueMerged, _PyXLMerged]] = dict()
    for issue in issue_merged:
        for pyxl in pyxl_merged:
            if pyxl.issue_name == issue.issue_name:
                yt_pyxl_paired[issue.issue_name] = (issue, pyxl)
    return yt_pyxl_paired


def unpaired(issue_merged: list[_IssueMerged], pyxl_merged: list[_PyXLMerged]) -> list[str]:
    """
    Get the unpaired YouTrack issue names.

    :param issue_merged: the _IssueMerged instances
    :type issue_merged: list[_IssueMerged]
    :param pyxl_merged: the _PyXLMerged instances
    :type issue_merged: list[_PyXLMerged]
    :return: the unpaired issue names.
    :rtype: list[str]
    """
    return [issue.issue_name for issue in issue_merged
            if not any(pyxl.issue_name == issue.issue_name for pyxl in pyxl_merged)]


def main():
    youtrack_config = UserConfig()
    user = User(youtrack_config)
    user.get_issue_work_items()
    user.get_issues()
    issue_merged = user.get_merged()

    path = youtrack_config.get_json_attr("path_table")
    wb = openpyxl.load_workbook(path)
    ws = wb["12 мес."]
    style_list = _StyleWorkItemList("styles")
    excel_prop = ExcelProp(ws, "excel_prop", style_list)
    pyxl_merged = excel_prop.get_merged()


if __name__ == "__main__":
    main()
