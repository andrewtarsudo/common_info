import openpyxl
from yt_config import UserConfig
from yt_requests import ConstYT, User, Issue, IssueWorkItem, _IssueMerged
from xl_table import ConstXL, ExcelProp, PyXLRow, PyXLWorkItem, _PyXLMerged
from _style_work_item import _StyleWorkItem, _StyleWorkItemList


def compare_merged(issue_merged: _IssueMerged, pyxl_merged: _PyXLMerged, instance: str) -> bool:
    issue: Issue = issue_merged.issue_item
    issue_work_items: list[IssueWorkItem] = issue_merged.work_items
    pyxl_row: PyXLRow = pyxl_merged.pyxl_row
    pyxl_items: list[PyXLWorkItem] = pyxl_merged.work_items

    if instance == "issue":
        issue_attrs = issue.issue, issue.state, issue.parent, issue.summary, issue.deadline
        pyxl_row_attrs = pyxl_row.issue, pyxl_row.state, pyxl_row.parent, pyxl_row.summary, pyxl_row.deadline
        return issue_attrs == pyxl_row_attrs

    if instance == "items":
        for work_item in issue_work_items:
            items_attrs = work_item.date, work_item.spent_time
            if any((pyxl_item.date, pyxl_item.spent_time) == items_attrs for pyxl_item in pyxl_items):
                continue
            else:
                return False
        return True


def create_pyxl_row(issue: Issue, excel_prop: ExcelProp):
    state = issue.state
    row = max(excel_prop.list_state_item(state)) + 1
    excel_prop.ws.insert_rows(row)
    excel_prop.ws[f"B{row}"].value = issue.parent
    excel_prop.ws[f"C{row}"].value = issue.issue
    excel_prop.ws[f"D{row}"].value = issue.summary
    excel_prop.ws[f"E{row}"].value = issue.deadline
    return PyXLRow(excel_prop.name, excel_prop.ws[f"C{row}"])


def create_pyxl_work_item(issue_work_item: IssueWorkItem, excel_prop: ExcelProp):
    
    return PyXLWorkItem()

def convert_issue_pyxlrow(issue_merged: _IssueMerged, pyxl_merged: _PyXLMerged):
    issue: Issue = issue_merged.issue_item
    work_items = issue_merged.work_items
    pass


def convert_pyxlrow_issue():
    pass


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
