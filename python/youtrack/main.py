import openpyxl
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from yt_config import UserConfig
from yt_requests import User
from xl_table import ExcelProp
from _style_work_item import _StyleWorkItemList
from openpyxl.styles.named_styles import NamedStyle
from join_user_excel import JoinUserXL


def convert_issue_state(state: str) -> str:
    """
    Converts the state to the table headers.

    :param str state: the issue state
    :return: the modified state.
    :rtype: str
    """
    dict_states = {
        "Active": "Active",
        "New": "New/Paused",
        "Paused": "New/Paused",
        "Canceled": "New/Paused",
        "Discuss": "New/Paused",
        "Done": "Done/Test",
        "Test": "Done/Test",
        "Review": "Done/Test",
        "Verified": "Verified",
        "Closed": "Verified"
    }
    if state in dict_states.keys():
        return dict_states[state]
    else:
        print(f"Unspecified state {state} is found.")
        return state


def add_styles(wb: Workbook, styles: _StyleWorkItemList):
    """
    Add the named styles to the Workbook styles.

    :param Workbook wb: the Workbook instance
    :param _StyleWorkItemList styles: the style list
    :return: None.
    """
    for style in styles:
        if not isinstance(style, NamedStyle):
            continue
        else:
            if style.name in wb.style_names:
                wb._named_styles.remove(style)
            wb._named_styles.append(style)
            style.bind(wb)


def main():
    youtrack_config = UserConfig()
    user = User(youtrack_config)
    user.pre_processing()

    path = youtrack_config.get_json_attr("path_table")
    copy_path = f"copy_{path}"
    wb: Workbook = openpyxl.load_workbook(path)
    ws: Worksheet = wb["12 мес."]
    style_list = _StyleWorkItemList("styles")
    add_styles(wb, style_list)

    excel_prop = ExcelProp(ws, "excel_prop", style_list)
    excel_prop.pre_processing()

    join_user_xl = JoinUserXL(user, excel_prop)
    join_user_xl.add_all_issues()
    join_user_xl.modify_all_issues()
    join_user_xl.add_new_work_items()
    join_user_xl.set_work_item_styles()

    print("The work is finished.")
    wb.save(f"copy_{user.path_table}")


if __name__ == "__main__":
    main()
