import datetime
import json
import pathlib
import re
import sys
from typing import Optional
from decimal import Decimal
import requests
import os
from numpy import divide, multiply
import numpy


dict_convert_logins: dict[str, str] = {'mozglyakova': 'matyushina'}
headers = {
    'Authorization': 'Bearer perm:dGFyYXNvdi1h.NjEtMTQw.1udDlV6zaAitHIgvw2eNQvF1sZ9JTZ',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}


def get_work_items(*, issue_name: str, person_name: str, date_period: Optional[str] = "{Last week}"):
    url = 'https://youtrack.protei.ru/api/workItems'
    parameters_fields = ','.join(('duration(minutes)', 'date'))

    if date_period is not None:
        parameters_query = ' '.join(
            (f'work author: {person_name}', f"work date: {date_period}", f"issue ID: {issue_name}")
        )
    else:
        parameters_query = ' '.join((f'work author: {person_name}', f"issue ID: {issue_name}"))

    params = (
        ('fields', parameters_fields),
        ('query', parameters_query),
    )

    requests.get(url=url, headers=headers, params=params)
    parsed_response = json.loads(requests.get(url=url, headers=headers, params=params).text)

    return parsed_response


def parse_yt_response(parsed_response: list[dict], flag: bool = True):
    res_pairs: list = []
    total_minutes: int = 0
    total_hours: float = 0

    if flag:
        for item in parsed_response:
            date = convert_long_datetime(item["date"])
            minutes = int(item["duration"]["minutes"])
            total_minutes = numpy.cumsum(minutes)
            total_hours = numpy.cumsum(divide(minutes, 60))
            result_string = f"date: {date}, minutes: {minutes}, hours: {Decimal(divide(minutes, 60))}"
            res_pairs.append(result_string)
    else:
        total_minutes: int = 0
        for item in parsed_response:
            minutes = int(item["duration"]["minutes"])
            total_minutes = numpy.cumsum(minutes)
            total_hours = numpy.cumsum(divide(minutes, 60))
            result_string = f"minutes: {minutes}, hours: {Decimal(divide(minutes, 60))}"
            res_pairs.append(result_string)
    res_pairs.append(f"Total sum minutes: {total_minutes}, total sum hours: {Decimal(total_hours)}.")

    return res_pairs


def convert_long_datetime(value) -> Optional[datetime.date]:
    """Converts the long value to the datetime.date."""
    if value is None:
        return None
    else:
        return datetime.date.fromtimestamp(multiply(value, 0.001))


def get_user():
    """
    Sets the UserYT based on the user parameters.\n
    :return: the user parameters of the UserYT type.
    """
    # get the path
    path: pathlib.Path = pathlib.Path().cwd()
    # get the user
    home_user: str = path.home().stem
    # check if the user and the login differ
    return dict_convert_logins[home_user] if home_user in dict_convert_logins else home_user


def verify_user(login: str):
    # check if the login is valid
    url = f"https://youtrack.protei.ru/user/{login}"
    params = ('fields', "login")

    return login if requests.get(url=url, headers=headers, params=params).ok else None


def parse_date_input(period_input: Optional[str]):
    print(period_input)
    if period_input is None or not period_input:
        print("ahaha")
        return "Last week"
    else:
        global_pattern = re.compile(r"(\d{2,4}.\d{2}.\d{2,4})\s\.\.\s(\d{2,4}.\d{2}.\d{2,4})")
        match = re.match(global_pattern, period_input)

        if match:
            date_start, date_end = match.group(0), match.group(1)
            return f"{convert_date_input(date_start)} .. {convert_date_input(date_end)}"
        else:
            print("test")
            return None


def convert_date_input(date_input: str):
    pattern_d_m_y = re.compile(r"(\d{2}).(\d{2}).(\d{4})")
    pattern_y_m_d = re.compile(r"(\d{4}).(\d{2}).(\d{2})")

    match_d_m_y = re.match(pattern_d_m_y, date_input)
    if match_d_m_y:
        return f"{match_d_m_y.group(2)}-{match_d_m_y.group(1)}-{match_d_m_y.group(0)}"

    match_y_m_d = re.match(pattern_y_m_d, date_input)
    if match_y_m_d:
        return f"{match_y_m_d.group(0)}-{match_y_m_d.group(1)}-{match_y_m_d.group(2)}"


def terminate_script(prompt: str):
    user_input = input(prompt)
    if user_input is None:
        return None
    else:
        modified_input = user_input.lower().strip()

        if user_input == "__exit__":
            sys.exit()
        else:
            return modified_input


def main():
    a = "None"
    print(parse_date_input(a))
    print("Print issue name.")
    user_issue_name = terminate_script("Format: {project}-{number}:\n")

    print("Print date period. Press Enter to use the default value.")
    print("Global format: {date_1} .. {date_2}. {date_1} - start date, {date_2} - end date.")
    print("Date format: YYYY{any_char}MM{any_char}DD or DD{any_char}MM{any_char}YYYY. "
          "DD - day, MM - month, YYYY - year.")
    user_date_period = terminate_script("Default date period is Last week:\n")

    while True:
        if user_date_period is None:
            date_period = "Last week"
            break
        elif parse_date_input(user_date_period) is None:
            user_date_period = terminate_script("Wrong dates. Try again.")
            print("w")
        else:
            date_period = parse_date_input(user_date_period)
            print("y")
            break

    login = get_user()
    print(login)

    while True:
        if verify_user(login) is None:
            login = terminate_script("Type the login:\n")
        else:
            break

    user_print_dates = terminate_script("Do you want to print the dates? Default: Yes. If No, print N.")
    dates_flag = user_print_dates.upper().strip() == "N"
    yt_response = get_work_items(issue_name=user_issue_name.upper(), person_name=login, date_period=date_period)
    print(parse_yt_response(yt_response, dates_flag))

    input("Press any key to close.")


if __name__ == "__main__":
    main()
