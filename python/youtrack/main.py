import openpyxl
from yt_config import UserConfig
from yt_requests import ConstYT, User, Issue, IssueWorkItem, _IssueMerged
from xl_table import ConstXL, ExcelProp, PyXLRow, PyXLWorkItem, _PyXLMerged
from _style_work_item import _StyleWorkItem, _StyleWorkItemList


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
