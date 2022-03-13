import pathlib
from typing import Union
import requests
import json
import datetime
from decimal import Decimal
import time
import codecs


class UserYT:
    """
    Displays parameters of the user in the YouTrack.
    """
    def __init__(self, login: str, auth_token: str):
        self._login = login
        self._auth_token = auth_token

    def __str__(self):
        return f"login = {self._login}, auth_token = {self._auth_token}"

    def __repr__(self):
        return f"UserYT(login={self._login}, auth_token = {self._auth_token})"

    @property
    def login(self):
        """Defines the login in the YouTrack."""
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def auth_token(self):
        """Defines the authentication token in the YouTrack."""
        return self._auth_token

    @auth_token.setter
    def auth_token(self, value):
        self._auth_token = value
        self.check_auth_token()

    @property
    def headers_user_yt(self):
        """
        Defines the headers for the requests. Contains the following headers: \n
        'Authorization': 'Bearer perm: self.auth_token',\n
        'Accept': 'application/json',\n
        'Content-Type': 'application/json'.\n
        :return: the headers parameters of the dict type.
        """
        bearer = ' '.join(('Bearer', self.auth_token))

        return {
            'Authorization': bearer,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def check_auth_token(self):
        """Adds the 'perm:' prefix to the authentication token if it is omitted."""
        if not self.auth_token.startswith('perm:'):
            upd_auth_token = ''.join(('perm:', self.auth_token))
            self.auth_token = upd_auth_token

    def write_auth_user_yt(self, path: pathlib.Path):
        """
        Defines the method to save the authentication parameters to the file.\n
        :param path: the path to the json file, pathlib.Path
        :return: None.
        """
        # set the data in the dict format
        dict_data = {
            "login": self.login,
            "auth_token": self.auth_token,
            "timestamp": str(datetime.date.today())
        }
        # set the data in the json format
        json_data = json.dumps(obj=dict_data, indent=2)
        # update the timestamp and close
        with open(path, 'w') as file:
            file.write(json_data)
            file.close()

    def get_issue_deadline(self, issue_name: str) -> datetime.date:
        """
        Defines the deadline of the issue from the YouTrack.\n
        :param issue_name: the issue identifier, idReadable, str
        :return: the issue deadline of the date type.
        """
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

    def get_work_items_deadline(self, date_period: str) -> list[tuple[str, datetime.date, int, datetime.date]]:
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
        parameters_query = ' '.join(('work author: me', f'work date: {date_period}'))
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


def read_auth_user_yt(path: pathlib.Path) -> UserYT:
    """
    Defines the method to read the authentication parameters from the file.\n
    :param path: the path to the file, pathlib.Path
    :return: the entity of the user with the authentication parameters of the UserYT type.
    """
    with open(path, 'r') as file:
        json_text = file.read()
        parsed_text: dict = json.loads(json_text)
        # check if the file contains the login and auth_token parameters
        if "login" not in parsed_text.keys() or "auth_token" not in parsed_text.keys():
            login, auth_token = "__nofile__", "__nofile__"
        else:
            # get the authentication parameters
            login, auth_token = parsed_text['login'], parsed_text['auth_token']

        return UserYT(login=login, auth_token=auth_token)


# define the default timestamp if the parameter is missing
today: datetime.date = datetime.date.today()
default_timestamp = f'{today.year}-01-01'


def read_auth_timestamp(path: pathlib.Path) -> str:
    """
    Defines the method to read the path to the table.\n
    :param path: the path to the file, pathlib.Path
    :return: the path to the xlsx table of the str type.
    """
    with open(path, 'r') as file:
        json_text = file.read()
        parsed_text: dict = json.loads(json_text)
    # check if the timestamp is defined in the file
    if 'timestamp' not in parsed_text.keys():
        return default_timestamp
    else:
        return parsed_text['timestamp']


def get_request(url: str, headers: dict, params: tuple) -> str:
    """
    Defines the GET request.\n
    If the initial input parameters are invalid, the exception is raised.\n
    :param url: URL to send the request, str
    :param headers: request headers, dict
    :param params: request parameters, tuple
    :return: the response text of the str type. If the exception is raised, the empty string is returned.
    """
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(e.__class__)
        print('The request demands on the proper URL, headers, and params.')
        return '{}'


def convert_long_datetime(value) -> datetime.date:
    """Converts the long value to the datetime.date."""
    if value is None:
        return datetime.date(year=1, month=1, day=1)
    else:
        return datetime.date.fromtimestamp(value // 1000)


# the dict of the deadline, state identifier in the query
dict_issue_name = {"ARCH_ST": '139-1028', "DOC_ST": '139-595', "ARCH": '139-1027', "DOC": '139-339', "VCST": '139-77'}


def define_deadline(issue_name: str) -> str:
    """
    Defines the deadline and state identifier in the query based on the issue name.\n
    :param issue_name: the name of the issue, str
    :return: the parameter identifier of the str type.
    """
    if issue_name.startswith('ARCH_ST'):
        key = 'ARCH_ST'
    elif issue_name.startswith('DOC_ST'):
        key = 'DOC_ST'
    elif issue_name.startswith('ARCH'):
        key = 'ARCH'
    elif issue_name.startswith('DOC'):
        key = 'DOC'
    elif issue_name.startswith('VCST'):
        key = 'VCST'
    else:
        key = None

    if key is not None:
        return dict_issue_name[key]
    else:
        return 'None'


def convert_work_items(
        list_work_items: list[tuple[str, datetime.date, int, datetime.date]],
        start_date: datetime.date,
        end_date: datetime.date):
    """
    Converts the list of work items to the printable form.\n
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

    while req_date <= end_date:
        list_final.append('----------')
        for issue_name, date, spent_time, deadline in list_work_items:
            # check if the date coincides with the required one
            if date == req_date:
                # define the spent time in hours for the table
                spent_time_hours = convert_spent_time(spent_time=spent_time)

                # add the strings to the list
                list_final.append(f'Дата: {date.strftime("%d %B %Y г")}')
                list_final.append(f'Задача: {issue_name}')
                list_final.append(f'Затраченное время: {spent_time} мин, для таблицы: {spent_time_hours} ч')

                # if the deadline is not specified
                if deadline == datetime.date(year=1, month=1, day=1):
                    list_final.append(f'Дедлайн/deadline: не задан\n')
                # if the deadline is specified
                else:
                    # define the readable deadline
                    deadline_readable = deadline.strftime("%d %B %Y г")
                    # define the deadline for the table
                    deadline_for_table = deadline.strftime("%d.%m.%Y")
                    list_final.append(f'Дедлайн/deadline: {deadline_readable}, для таблицы: {deadline_for_table}')
        req_date += datetime.timedelta(days=1)

    return list_final


def convert_spent_time(spent_time: int) -> Union[int, Decimal]:
    """
    Converts the spent time in minutes to hours.\n
    :param spent_time: the spent time in minutes, int
    :return: the converted spent time of the decimal or the int type.
    """
    if spent_time % 60 == 0:
        return spent_time // 60
    else:
        return Decimal(spent_time / 60).normalize()


def check_json_file(path: pathlib.Path) -> bool:
    """
    Checks if the JSON file exists.\n
    :param path: the path to the json file, pathlilb.Path
    :return: the file existence flag of the bool type. 
    """
    try:
        with open(path, 'w+') as file:
            file.close()
    except FileNotFoundError:
        print('Файл youtrack.json не найден. Программа прекращает работу.')
        return False
    except PermissionError:
        print('Возникла проблема с правами доступа. Программа прекращает работу.')
        return False
    except OSError as e:
        print(f'Возникла ошибка {e.__class__.__name__}. Программа прекращает работу.')
        print('Сообщите о полученной ошибке для исправления кода. Спасибо.')
        return False
    else:
        return True


def terminate_script(string: str):
    """Set the value to terminate the program in any input to ignore any loops or KeyInterruptError."""
    if string.strip() == '__exit__':
        print('Работа прервана. Программа закрывается.')
        exit()


def main():
    # path to the json file
    path = pathlib.Path('./youtrack.json').resolve()
    # check if the youtrack.json file exists
    if not check_json_file(path):
        time.sleep(3)
        input('Нажмите любую клавишу, чтобы закрыть программу.\n')
        exit()
    # get the authorization parameters for the UserYT
    user: UserYT = read_auth_user_yt(path)
    # read the timestamp
    timestamp: str = read_auth_timestamp(path)

    # define the announcement
    print('Введите интервал для вывода работ, зафиксированных в YouTrack.')
    print(f'По умолчанию запрос делается для промежутка с момента последнего запуска {timestamp} до сегодняшнего дня')
    print('Для этого далее нажимайте "Enter".')

    # set the period for requests
    # define the first date in the period
    first_date_input = input('Введите начальную дату интервала в формате ГГГГ-ММ-ДД или нажмите "Enter":\n')
    terminate_script(first_date_input)
    # check if the input is correct
    try:
        first_datetime = datetime.datetime.fromisoformat(first_date_input.strip())
    except ValueError:
        print(f'Введенное значение некорректно. Будет использовано значение по умолчанию {timestamp}.')
        first_datetime = datetime.datetime.fromisoformat(timestamp)
    except Exception as e:
        print(f'Ошибка {e.__class__.__name__}. Будет использовано значение по умолчанию {timestamp}.')
        print('Сообщите о полученной ошибке для исправления кода. Спасибо.')
        first_datetime = datetime.datetime.fromisoformat(timestamp)
    else:
        # if the input is empty
        if first_date_input.strip():
            # apply the default values if empty
            print(f'Будет использовано значение по умолчанию {timestamp}.')
            first_datetime = datetime.datetime.fromisoformat(timestamp)

    first_date = str(first_datetime.date())
    # define the last date in the period
    last_day_input = input('Введите конечную дату интервала в формате ГГГГ-ММ-ДД или нажмите "Enter":\n')
    terminate_script(last_day_input)
    # check if the input is correct
    try:
        last_datetime = datetime.datetime.fromisoformat(last_day_input.strip())
        last_date = str(last_datetime.date())
    except ValueError:
        print(f'Введенное значение некорректно. Будет использовано значение по умолчанию {datetime.date.today()}.')
        last_datetime = datetime.datetime.today()
        last_date = 'Today'
    except Exception as e:
        print(f'Ошибка {e.__class__.__name__}. Будет использовано значение по умолчанию {datetime.date.today()}.')
        print('Сообщите о полученной ошибке для исправления кода. Спасибо.')
        last_datetime = datetime.datetime.today()
        last_date = 'Today'
    else:
        # if the input is empty
        if last_day_input.strip():
            # apply the default values if empty
            print(f'Будет использовано значение по умолчанию {datetime.date.today()}.')
            last_datetime = datetime.datetime.today()
            last_date = 'Today'

    # set the string for the period
    # check the input dates if the period is proper, the default one is not checked
    if (first_date, last_date) != (timestamp, datetime.date.today()) and first_date > last_date:
        # the period is improper
        print('Введенный промежуток некорректен. Будет использован промежуток по умолчанию:')
        print(f'{timestamp} .. {datetime.date.today()}')
        date_period: str = f'{timestamp} .. {datetime.date.today()}'
    else:
        date_period: str = f'{first_date} .. {last_date}'

    # get all YouTrack WorkItem entities
    list_work_items = user.get_work_items_deadline(date_period=date_period)
    # define the period
    start_date = first_datetime.date()
    end_date = last_datetime.date()
    # convert the info to the readable format
    printable_res = convert_work_items(list_work_items=list_work_items, start_date=start_date, end_date=end_date)

    # update the timestamp
    user.write_auth_user_yt(path=path)
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
        if save_input.strip():
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

            # combine the file name
            path_file = str(save_input) + '.txt'

            # check if the file exists
            if not pathlib.Path(f'./{path_file}').resolve().exists():
                # if it does not exist
                flag = False
                # create the file, write the results, and close
                with open(path_file, 'w+', encoding="cp1251") as file:
                    file.writelines(readable_printable_res)
                    print(f"Файл {save_input}.txt создан.")
                    file.close()
            else:
                # if it exists
                print('Такой файл уже существует, перезаписать его? По умолчанию - нет.')
                approve_input = input('Y или Д - да / N или Н - нет.\n')
                terminate_script(approve_input)
                # check the approval
                if not approve_input.strip() and approve_input.strip().lower() in ('y', 'д'):
                    # rewrite the file
                    flag = False
                    # write the results instead of the file contents and close
                    with open(path_file, 'w+', encoding="cp1251") as file:
                        file.writelines(readable_printable_res)
                        print(f"Файл {save_input}.txt перезаписан.")
                        file.close()
                # not to rewrite the file, start the cycle again
                else:
                    continue


if __name__ == '__main__':
    main()
