import pathlib
import re
import requests
import json
import datetime
import decimal
import time
import codecs

# logins that may use it
reg_logins = ('kuksina', 'matyushina', 'brovko', 'lyalina', 'demyanenko', 'nikitina', 'mazyarova', 'fesenko', 'nigrej',
              'vykhodtsev', 'bochkova', 'tarasov-a')
# possible differences in names and logins
dict_convert_logins: dict[str, str] = {'mozglyakova': 'matyushina'}

date_today = datetime.date.today()
timestamp = datetime.date(year=date_today.year, month=1, day=1)
default_timestamp = timestamp.strftime('%Y-%m-%d')
today = 'Today'


class UserYT:
    """
    Displays parameters of the user in the YouTrack.
    """
    def __init__(self, login: str = '__nologin__'):
        self._login = login

    def __str__(self):
        return f"login = {self._login}"

    def __repr__(self):
        return f"UserYT(login={self._login})"

    @property
    def login(self):
        """Defines the login in the YouTrack based on the account name."""
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def headers_user_yt(self):
        """
        Defines the headers for the requests. Contains the following headers:\n
        'Authorization': 'Bearer perm: auth_token',\n
        'Accept': 'application/json',\n
        'Content-Type': 'application/json'.\n
        :return: the headers parameters of the dict type.
        """
        return {
            'Authorization': 'Bearer perm:dGFyYXNvdi1h.NjEtMTQw.1udDlV6zaAitHIgvw2eNQvF1sZ9JTZ',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def get_issue_deadline(self, issue_name: str) -> datetime.date:
        """
        Defines the deadline of the issue from the YouTrack.\n
        :param issue_name: the issue identifier, idReadable, str
        :return: the issue deadline of the date type.
        """
        # get the identifier of the deadline for the issue project
        deadline_identifier = define_deadline(issue_name)

        if deadline_identifier == 'None':
            return datetime.date(year=1, month=1, day=1)
        else:
            # define the parameters of the request
            url = f'https://youtrack.protei.ru/api/issues/{issue_name}/customFields/{deadline_identifier}'
            headers = self.headers_user_yt
            params = (('fields', 'value(name)'),)
            # get the response in the JSON format
            parsed_response = json.loads(get_request(url=url, headers=headers, params=params))

            return convert_long_datetime(parsed_response['value'])

    def get_work_items(self, date_period: str) -> list[tuple[str, datetime.date, int, datetime.date]]:
        """
        Defines the dict of the work issue parameters: issue_name, date, spent_time.\n
        :param date_period: the period of creating the work issue item, YYYY-MM-DD/YYYY-MM, str
        :return: the work issue parameters of the dict[str, list[str, date, int, date]] type.
        """
        list_work_items: list[tuple[str, datetime.date, int, datetime.date]] = list()
        # define the parameters of the request
        url = 'https://youtrack.protei.ru/api/workItems'
        headers = self.headers_user_yt
        parameters_fields = ','.join(('duration(minutes)', 'date', 'issue(idReadable)'))
        parameters_query = ' '.join((f'work author: {self.login}', f'work date: {date_period}'))
        params = (
            ('fields', parameters_fields),
            ('query', parameters_query),
        )
        # get the response in the JSON format
        parsed_response = json.loads(get_request(url=url, headers=headers, params=params))

        for item in parsed_response:
            # define the issue name of the work item
            issue_name: str = item['issue']['idReadable']
            # define the date of the work item
            date: datetime.date = convert_long_datetime(item['date'])
            # define the spent time of the work item
            spent_time: int = item['duration']['minutes']
            # define the default deadline
            deadline: datetime.date = self.get_issue_deadline(issue_name=issue_name)

            list_work_items.append((issue_name, date, spent_time, deadline))

        return list_work_items


def get_user() -> UserYT:
    """
    Sets the UserYT based on the user parameters.\n
    :return: the user parameters of the UserYT type.
    """
    # get the path
    path: pathlib.Path = pathlib.Path().cwd()
    # get the user
    home_user: str = path.home().stem
    # check if the user and the login differ
    login = dict_convert_logins[home_user] if home_user in dict_convert_logins.keys() else home_user
    # check if the login is valid
    if login in reg_logins:
        return UserYT(login=home_user)
    else:
        return UserYT(login='__nologin__')


def get_request(url: str, headers: dict, params: tuple) -> str:
    """
    Defines the GET request.\n
    If the initial input parameters are invalid, the exception is raised.\n
    :param url: URL to send the request, str
    :param headers: request headers, dict
    :param params: request parameters, tuple
    :return: the response text of the str type. If the exception is raised, the empty string is returned.
    """
    print(f'url = {url}, headers = {headers}, params = {params}')
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f'Ошибка {e.__class__.__name__}. Некорректные параметры URL, headers и params.')
        input('Нажмите на любую клавишу, чтобы завершить работу')
        exit()
    else:
        return response.text


def convert_long_datetime(value: int) -> datetime.date:
    """
    Converts the long value to the datetime.date.\n
    :param value: the integer to convert, int
    :return: the associated date of the date type.
    """
    if value is None:
        return datetime.date(year=2021, month=1, day=1)
    else:
        return datetime.date.fromtimestamp(value // 1000)


# the dict of the deadline, state identifier in the query
dict_issue_name = {"ARCH_ST": '139-1028', "DOC_ST": '139-595', "ARCH": '139-1027', "DOC": '139-339', "VCST": '139-77'}


def define_deadline(issue_name: str) -> str:
    """
    Defines the deadline identifier in the query based on the issue name.\n
    :param issue_name: the name of the issue, str
    :return: the parameter identifier, str
    """
    print(f'issue_name = {issue_name}')
    if not re.match(r'[A-Z_]*-\d+', issue_name.upper()):
        return 'None'
    # separate project with _ST and without it
    list_st: list[str] = [project for project in dict_issue_name.keys() if re.match(r'\w{3,4}_ST', project)]
    list_other: list[str] = [project for project in dict_issue_name.keys() if project not in list_st]
    # check if the issue project has _ST
    if any(issue_name.startswith(project_st) for project_st in list_st):
        for project_st in list_st:
            if issue_name.startswith(project_st):
                return dict_issue_name[project_st]
    # check if the issue project has no _ST
    elif any(issue_name.startswith(project_other) for project_other in list_other):
        for project_other in list_other:
            if issue_name.startswith(project_other):
                return dict_issue_name[project_other]
    # if smth went wrong
    else:
        return 'None'


def convert_work_items(
        list_work_items: list[tuple[str, datetime.date, int, datetime.date]],
        start_date: datetime.date,
        end_date: datetime.date):
    """
    Converts the list of work items to the printable format.\n
    :param list_work_items: the dict with the work items, list[tuple[str, date, int, date]]
    :param start_date: the first day of the period, date
    :param end_date: the last day of the period, date
    :return: the list of readable strings of the list[str] type.
    """
    # issue_name, date, spent_time(minutes), deadline
    list_final: list[str] = list()
    # define the start point
    req_date: datetime.date = start_date
    # add the empty string
    print('\n')

    list_final.append('----------')

    while req_date <= end_date:
        if any(date == req_date for issue_name, date, spent_time, deadline in list_work_items):
            for issue_name, date, spent_time, deadline in list_work_items:
                # check if the date coincides with the required one
                if date == req_date:
                    # define the spent time in hours for the table
                    spent_time_hours = convert_spent_time(spent_time=spent_time)

                    # add the strings to the list

                    list_final.append(f'Дата: {date.strftime("%d %B %Y г")}')
                    list_final.append(f'Задача: {issue_name}')
                    list_final.append(f'Затраченное время: {spent_time} мин, для таблицы: {spent_time_hours} ч\n')

                    # if the deadline is not specified
                    if deadline == datetime.date(year=1, month=1, day=1):
                        list_final.append(f'Дедлайн/deadline: не задан\n')
                    # if the deadline is specified
                    else:
                        # define the readable deadline
                        deadline_readable = deadline.strftime("%d %B %Y г")
                        # define the deadline for the table
                        deadline_for_table = deadline.strftime("%d.%m.%Y")
                        list_final.append(f'Дедлайн/deadline: {deadline_readable}, для таблицы: {deadline_for_table}\n')

            list_final.append('----------')

        req_date += datetime.timedelta(days=1)

    return list_final


def convert_date_iso(input_date: str) -> str:
    """
    Converts different date formats to the ISO standard.\n
    :param input_date: the date to convert, str
    :return: the modified date of the str type.
    """
    date_conversion_rules = (
        (re.compile(r'(\d{4}).(\d{1,2}).(\d{1,2})'), (1, 2, 3)),
        (re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})'), (3, 2, 1))
    )
    print(f'input_date = {input_date}')
    # if the date format is not specified
    if not any(re.match(pattern, input_date) for pattern, match in date_conversion_rules):
        return 'None'

    for pattern, group_match in date_conversion_rules:
        match = re.match(pattern, input_date)
        # find the pattern to convert
        if match:
            i_1, i_2, i_3 = group_match
            print(f'i_1, i_2, i_3 = {i_1}, {i_2}, {i_3}')

            return f'{match.group(i_1)}-{match.group(i_2)}-{match.group(i_3)}'


def convert_spent_time(spent_time: int):
    """
    Converts the spent time in minutes to hours.\n
    :param spent_time: the spent time in minutes, int
    :return: the converted spent time of the decimal or the int type.
    """
    if spent_time % 60 == 0:
        return spent_time // 60
    else:
        return decimal.Decimal(spent_time / 60).normalize()


# the commands to stop the program
terminate_commands = ('__exit__', '"__exit__"', "'__exit__'")


def terminate_script(string: str):
    """Set the value to terminate the program in any input to ignore any loops and KeyInterruptError."""
    if string.lower().strip() in terminate_commands:
        print('Работа прервана. Программа закрывается.')
        exit()


def main():
    user: UserYT = get_user()
    print(f'user = {user}')

    while True:
        # check if the login is not specified
        if user.login == '__nologin__':
            login_input = input('Не удалось определить пользователя. Введите логин пользователя на YouTrack.\n')
            login_input_upd = login_input.lower().strip()
            terminate_script(login_input_upd)
            # verify the new login from the input
            if login_input_upd in reg_logins:
                user.login = login_input_upd
                break
            else:
                print('Введенный логин не совпадает ни с одним из предусмотренных. Введите логин еще раз.\n')
        else:
            break

    # define the announcement
    print('Введите интервал для вывода работ, зафиксированных в YouTrack.')
    print(f'По умолчанию запрос делается для промежутка с {default_timestamp} до сегодняшнего дня')
    print('Для этого далее нажимайте "Enter".')

    # indicate if the attempt to type the start date is the first
    first_try = True
    # flag for the cycle
    flag = True
    # the default start date
    start_string: str = default_timestamp
    start_date: datetime.date = timestamp

    while flag:
        # the text for the date input
        if first_try:
            prompt = 'Введите начальную дату интервала в формате ГГГГ ММ ДД или ДД ММ ГГГГ или нажмите "Enter":\n'
        # the text after the faile login change
        else:
            prompt = 'Введенный логин не зарегистрирован на YouTrack. Повторите ввод:\n'

        first_date_input = input(prompt)
        terminate_script(first_date_input)
        # the first try is over
        first_try = False
        # check if the user wants to change the login
        if first_date_input.lower().strip().startswith('login '):
            new_login: str = first_date_input[6:].lower().strip()
            if new_login in dict_convert_logins.keys():
                new_login_upd = dict_convert_logins[new_login]
            else:
                new_login_upd = dict_convert_logins[new_login]
            # verify the new login
            if new_login_upd in reg_logins:
                # change the login
                user.login = new_login
                print(f'Логин изменен на {new_login}.')
                first_try = True
            else:
                continue
        else:
            flag = False
            # check if the input is empty
            if not first_date_input:
                print(f'first_date_input = {first_date_input}')
                # apply the default values if empty
                print(f'Будет использовано значение по умолчанию {default_timestamp}.')
            else:
                try:
                    # convert the input date
                    start_string: str = convert_date_iso(first_date_input)
                except ValueError:
                    print(f'Введенное значение некорректно.')
                    print(f'Будет использовано значение по умолчанию {default_timestamp}.')
                else:
                    start_date: datetime.date = datetime.date.fromisoformat(start_string)

    # the default end date
    end_date: datetime.date = date_today
    end_string: str = today

    # define the last date in the period
    last_day_input = input('Введите конечную дату интервала в формате ГГГГ-ММ-ДД или ДД ММ ГГГГ или нажмите "Enter":\n')
    terminate_script(last_day_input)
    # check if the input is empty
    if not last_day_input:
        # apply the default values if empty
        print(f'Будет использовано значение по умолчанию {date_today}.')
    else:
        try:
            # convert the input date
            end_string = convert_date_iso(last_day_input)
        except ValueError:
            print(f'Введенное значение некорректно. Будет использовано значение по умолчанию {date_today}.')
        else:
            end_date = datetime.date.fromisoformat(end_string)

    # set the string for the period
    date_period: str = f'{start_string} .. {end_string}'
    print(f'date_period = {date_period}')
    # get all YouTrack WorkItem entities
    list_work_items = user.get_work_items(date_period=date_period)
    # convert the info to the readable format
    printable_res = convert_work_items(list_work_items=list_work_items, start_date=start_date, end_date=end_date)

    # print the results
    for string in printable_res:
        print(string)

    # flag for the cycle
    flag = True
    # save the results to the file
    while flag:
        # ask to save the results to the file
        print('\nСохранить в файл txt? Нажмите "Enter", чтобы закрыть без сохранения немедленно.')
        save_input = input('Для записи в файл введите название файла без расширения:\n')
        terminate_script(save_input)
        # not to save the results
        if not save_input.strip():
            # terminate the program
            print('Завершается работа ...')
            time.sleep(1)
            exit()
        else:
            readable_printable_res = []
            # convert to the readable format
            for string in printable_res:
                # add the rule to start the next string from the next line
                upd_string = string + '\n'
                # required for supporting Russian
                string_encoded = codecs.encode(upd_string, "cp1251")
                # required for proper printing
                readable_printable_res.append(string_encoded.decode("cp1251"))
            # delete the extension
            if save_input.strip().endswith('.txt'):
                save_input_upd: str = save_input[:-4].strip()
            else:
                save_input_upd = save_input.strip()
            print(f'save_input_upd = {save_input_upd}')
            # combine the file name
            path_file = pathlib.Path().cwd() / f'{save_input_upd}.txt'

            # check if the file exists
            if not path_file.exists():
                # if it does not exist
                flag = False
                # create the file, write the results, and close
                with open(path_file, 'w+', encoding="cp1251") as file:
                    file.writelines(readable_printable_res)
                    file.close()
                    print(f"Файл {save_input_upd}.txt создан.")
                    input('Нажмите любую клавишу для закрытия программы.\n')
                    exit()
            else:
                # if it exists
                print('Такой файл уже существует, перезаписать его? По умолчанию - нет.')
                approve_input = input('Y или Д - да / N или Н - нет.\n')
                terminate_script(approve_input)
                # not to rewrite the file, start the cycle again
                if not approve_input.strip() or approve_input.lower().strip() in ('n', 'н'):
                    continue
                else:
                    # rewrite the file
                    flag = False
                    # write the results instead of the file contents and close
                    with open(path_file, 'w+', encoding="cp1251") as file:
                        file.writelines(readable_printable_res)
                        file.close()
                        print(f"Файл {save_input}.txt перезаписан.")
                        input('Нажмите любую клавишу для закрытия программы.\n')
                        exit()


if __name__ == '__main__':
    main()
