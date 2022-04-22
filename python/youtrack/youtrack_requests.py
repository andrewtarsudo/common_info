import pathlib
import re
from typing import Union, Optional
import numpy
import requests
import json
import datetime


class ConstYT:
    dict_issue = dict()
    dict_issue_work_item = dict()

    dict_issue_name = {
        "ARCH_ST": ('139-1028', '67-2494'),
        "DOC_ST": ('139-595', '67-1426'),
        "ARCH": ('139-1027', '67-2487'),
        "DOC": ('139-339', '67-1127'),
        "VCST": ('139-77', '67-353')
    }
    # the dict of the deadline, state identifier in the query
    terminate_commands = ('__exit__', '"__exit__"', "'__exit__'")


def convert_date_iso(input_date: str) -> Optional[datetime.date]:
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
        return None

    for pattern, group_match in date_conversion_rules:
        match = re.match(pattern, input_date)
        # find the pattern to convert
        if match:
            i_1, i_2, i_3 = group_match
            date_iso = f'{match.group(i_1)}-{match.group(i_2)}-{match.group(i_3)}'
            return datetime.date.fromisoformat(date_string=date_iso)


def convert_spent_time(spent_time: int) -> Union[int, float]:
    """
    Converts the spent time in minutes to hours.\n
    :param spent_time: the spent time in minutes, int
    :return: the converted spent time of the Union[int, Decimal] type.
    """
    return numpy.divide(spent_time, 60)


def convert_issue_state(state: str) -> str:
    """
    Converts the state to the table headers.\n
    :param state: the issue state, str
    :return: the modified state of the str type.
    """
    # the issues to convert to the New/Paused
    to_new_paused = ('New', 'Paused', 'Canceled', 'Discuss', '', 'New/Paused')
    # the issues to convert to the Done/Test
    to_done_test = ('Done', 'Test', 'Review', 'Done/Test')
    # the issues to convert to the Verified
    to_verified = ('Closed',)

    if state in to_new_paused:
        modified_state = 'New/Paused'
    elif state in to_done_test:
        modified_state = 'Done/Test'
    elif state in to_verified:
        modified_state = 'Verified'
    else:
        modified_state = state

    return modified_state


def check_terminate_script(prompt: str) -> str:
    """
    Check the input to terminate the program.\n
    :param prompt: the text to display, str
    :return: either exit() or modified command of the str type.
    """
    user_input = input(prompt)
    # delete trailing zeros and lower case
    user_command = user_input.lower().strip()

    if user_command in ConstYT.terminate_commands:
        print('Работа прервана. Программа закрывается.')
        exit()
    else:
        return user_command


def convert_datetime_long(value: datetime.date):
    """Converts the date value to the long."""
    date_and_time = datetime.datetime.combine(value, datetime.time.min)
    timestamp = datetime.datetime.timestamp(date_and_time)
    return int(timestamp)


def define_deadline_state(issue_name: str, res: str) -> Optional[str]:
    """
    Defines the deadline and state identifier in the query based on the issue name.\n
    :param issue_name: the name of the issue, str
    :param res: the required identifier, str
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
        if res == 'deadline':
            return ConstYT.dict_issue_name[key][0]
        elif res == 'state':
            return ConstYT.dict_issue_name[key][1]
    else:
        return None


class User:
    __headers_yt = {
        'Authorization': 'Bearer perm:dGFyYXNvdi1h.NjEtMTQw.1udDlV6zaAitHIgvw2eNQvF1sZ9JTZ',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    __dict_convert_logins: dict[str, str] = {'mozglyakova': 'matyushina'}

    default_format = "%Y-%m-%d"
    default_timestamp: str = datetime.date(year=datetime.date.today().year, month=1, day=1).strftime(default_format)
    default_period: str = f"{default_timestamp} .. Today"

    def __init__(self, timestamp: datetime.date = default_timestamp):
        self.timestamp = timestamp

    def __str__(self):
        return f"User: login = {self.login}, timestamp = {self.timestamp}"

    def __repr__(self):
        return f"User(login={self.login}, timestamp={self.timestamp})"

    def __key(self):
        return self.login, self.timestamp

    def __eq__(self, other):
        if isinstance(other, User):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, User):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.login, self.timestamp))

    @property
    def login(self):
        _sys_login: str = pathlib.Path.home().stem
        login = User.__dict_convert_logins[_sys_login] if _sys_login in User.__dict_convert_logins else _sys_login

        url = f"https://youtrack.protei.ru/api/users/{login}"
        params = (('fields', 'login'),)

        if requests.get(url=url, headers=User.__headers_yt, params=params).ok:
            return login
        else:
            return None

    @property
    def verify_login(self) -> bool:
        """
        Verifies the login.\n
        :return: the response of the attempt request of the bool type.
        """
        if self.login is not None:
            url = f"https://youtrack.protei.ru/api/users/{self.login}"
            params = (('fields', 'login'),)
            try:
                requests.get(url=url, headers=User.__headers_yt, params=params).raise_for_status()
            except requests.HTTPError:
                return False
            except OSError as e:
                print(f'Получена ошибка {e.errno}, {e.strerror}. Логин некорректен.')
                return False
            else:
                return True
        else:
            return False

    def get_issues(self, date_period: str = default_period) -> dict[str, list[str, str, str, datetime.date, str]]:
        """
        Defines the dict of the issues parameters: parent, name, summary, deadline, state, work_items.\n
        :param date_period: the update period of the issue, YYYY-MM-DD/YYYY-MM, str
        :return: the issue parameters of the dict[str, list[str, str, str, date, str, list]] type.
        """
        dict_issues = dict()
        # define the parameters of the request
        url = 'https://youtrack.protei.ru/api/issues'
        parameters_fields = ','.join(('idReadable', 'summary', 'parent(issues(idReadable))'))
        parameters_query = ' '.join((f'assignee: {self.login}', f'updated: {date_period}'))
        params = (
            ('fields', parameters_fields),
            ('query', parameters_query),
        )
        # get the response in the JSON format
        parsed_response = json.loads(get_request(url=url, headers=User.__headers_yt, params=params))
        # define the parameters of the issue
        for item in parsed_response:
            name, parent, summary, deadline, state = self.parse_response_issue(item)
            dict_issues[name] = [parent, name, summary, deadline, state]

        return dict_issues

    def get_issue_deadline(self, issue_name: str) -> datetime.date:
        """
        Defines the deadline of the issue from the YouTrack.\n
        :param issue_name: the issue identifier, idReadable, str
        :return: the issue deadline of the date type.
        """
        deadline_identifier = define_deadline_state(issue_name, 'deadline')
        deadline: datetime.date = datetime.date(1, 1, 1)

        if deadline_identifier != 'None':
            # define the parameters of the request
            url = f'https://youtrack.protei.ru/api/issues/{issue_name}/customFields/{deadline_identifier}'
            params = (('fields', 'value(name)'),)
            # get the response in the JSON format
            parsed_response: dict = json.loads(get_request(url=url, headers=self.__headers_yt, params=params))

            if "value" in parsed_response.keys():
                deadline = convert_long_datetime(parsed_response['value'])

        return deadline

    def get_issue_state(self, issue_name: str) -> str:
        """
        Defines the state of the issue from the YouTrack.\n
        :param issue_name: the issue identifier, idReadable, str
        :return: the issue state of the str type.
        """
        state_identifier = define_deadline_state(issue_name, 'state')
        state = ''

        if state_identifier != 'None':
            # define the parameters of the request
            url = f'https://youtrack.protei.ru/api/issues/{issue_name}/customFields/{state_identifier}'
            params = (('fields', 'value(name)'),)
            # get the response in the JSON format
            parsed_response = json.loads(get_request(url=url, headers=self.__headers_yt, params=params))

            if "value" in parsed_response.keys() and "name" in parsed_response["value"].keys():
                state = convert_issue_state(parsed_response['value']['name'])

        return state

    def get_issue_work_items(self, date_period: str) -> \
            dict[str, list[tuple[str, datetime.date, Union[int, float]]]]:
        """
        Defines the dict of the work issue parameters: name, date, spent_time.\n
        :param date_period: the period of creating the work issue item, YYYY-MM-DD/YYYY-MM, str
        :return: the dict of the work issues of the dict[str, list[tuple[str, date, Union[int, decimal]]]] type.
        """
        dict_work_items: dict[str, list[tuple[str, datetime.date, Union[int, float]]]] = dict()
        # define the parameters of the request
        url = 'https://youtrack.protei.ru/api/workItems'
        parameters_fields = ','.join(('duration(minutes)', 'date', 'issue(idReadable)'))
        parameters_query = ' '.join((f'work author: {self.login}', f'work date: {date_period}'))
        params = (
            ('fields', parameters_fields),
            ('query', parameters_query),
        )
        # get the response in the JSON format
        parsed_response = json.loads(get_request(url=url, headers=self.__headers_yt, params=params))

        for item in parsed_response:
            issue_name, date, modified_spent_time = self.parse_response_work_item(item)
            dict_work_items[issue_name].append((issue_name, date, modified_spent_time))

        return dict_work_items

    @staticmethod
    def parse_response_work_item(item: dict):
        # define the issue name of the work item
        issue_name = item['issue']['idReadable']
        # define the date of the work item
        date = convert_long_datetime(item['date'])
        # define the spent time of the work item
        spent_time = item['duration']['minutes']
        # convert to the hours
        modified_spent_time = convert_spent_time(spent_time)
        return issue_name, date, modified_spent_time

    def get_issue_id(self, issue_name: str) -> tuple[str, str, str, datetime.date, str]:
        """
        Defines the dict of the issue parameters: parent, name, summary, deadline, state, work_items.\n
        :param issue_name: the issue name, str
        :return: the issue parameters of the dict[str, list[str, str, str, date, str]] type.
        """
        # define the parameters of the request
        url = f'https://youtrack.protei.ru/api/issues/{issue_name}'
        parameters_fields = ','.join(('idReadable', 'summary', 'parent(issues(idReadable))'))
        params = (('fields', parameters_fields),)
        # get the response in the JSON format
        parsed_response = json.loads(get_request(url=url, headers=self.__headers_yt, params=params))
        return self.parse_response_issue(parsed_response)

    def parse_response_issue(self, item: dict):
        # define the issue name
        name: str = item['idReadable']
        # define the parent issue name
        parent_issues = item['parent']['issues']
        # check if the parent issue __exists
        if len(parent_issues):
            parent: Optional[str] = parent_issues[0]['idReadable']
        else:
            parent = None
        # define the issue summary
        summary: str = item['summary']
        # define the issue deadline
        deadline = self.get_issue_deadline(name)
        # define the issue state
        state = self.get_issue_state(name)
        # define the dictionary of the issue
        return name, parent, summary, deadline, state


class Issue:
    """Displays parameters of the issue in the YouTrack."""
    index = 0

    __slots__ = ("identifier", "name", "state", "summary", "parent", "deadline", "commentary")

    def __init__(self,
                 name: str, *,
                 state: str = None,
                 summary: str = None,
                 parent: str = None,
                 deadline: datetime.date = None,
                 commentary: str = None):
        self.identifier = Issue.index
        self.name = name
        self.state = state
        self.summary = summary
        self.parent = parent
        self.deadline = deadline
        self.commentary = commentary

        ConstYT.dict_issue[self.identifier] = self
        Issue.index += 1

    def __str__(self):
        return f"id = {self.identifier}, name = {self.name}, state = {self.state}, summary = {self.summary}," \
               f"parent = {self.parent}, deadline = {self.deadline}"

    def __repr__(self):
        return f"Issue(name = {self.name}, state = {self.state}, summary = {self.summary}, parent = {self.parent}, " \
               f"deadline = {self.deadline}, commentary={self.commentary}), id={self.identifier}"

    def __key(self):
        return self.index, self.name

    def __eq__(self, other):
        if isinstance(other, Issue):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Issue):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.identifier, self.name, self.state, self.summary, self.parent, self.deadline, self.commentary))


class IssueWorkItem:
    index = 0

    __slots__ = ("identifier", "name", "date", "spent_time")

    def __init__(self, name: str, date: datetime.date, spent_time: int):
        self.identifier = IssueWorkItem.index
        self.name = name
        self.date = date
        self.spent_time = spent_time

        ConstYT.dict_issue_work_item[self.identifier] = self
        IssueWorkItem.index += 1

    def __str__(self):
        return f"IssueWorkItem: name = {self.name}, date = {self.date}, spent_time = {self.spent_time}, " \
               f"id: {self.identifier}"

    def __repr__(self):
        return f"IssueWorkItem(name = {self.name}, date = {self.date}, spent_time = {self.spent_time}), " \
               f"identifier={self.identifier}"

    def __key(self):
        return self.name, self.date

    def __hash__(self):
        return hash((self.identifier, self.name, self.date, self.spent_time))

    def __eq__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __combine(self, other) -> Optional[int]:
        if self == other:
            self.spent_time += other.spent_time
            del other.spent_time
            return self.identifier
        else:
            return None

    def __lt__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.date < other.date
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.date > other.date
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.date <= other.date
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.date >= other.date
        else:
            return NotImplemented


class _IssueMerged:
    __slots__ = ("issue_name",)

    def __init__(self, issue_name: str):
        self.issue_name = issue_name

    @property
    def issue(self) -> int:
        issue: Issue
        for issue_id, issue in ConstYT.dict_issue.items():
            if self.issue_name == issue.name:
                return issue_id

    @property
    def work_items(self) -> list[int]:
        work_item: IssueWorkItem
        return [work_item_id for work_item_id, work_item in ConstYT.dict_issue_work_item.items()
                if self.issue_name == work_item.name]

    def __hash__(self):
        return hash(self.issue_name)

    def __eq__(self, other):
        if isinstance(other, _IssueMerged):
            return self.issue_name == other.issue_name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _IssueMerged):
            return self.issue_name != other.issue_name
        else:
            return NotImplemented

    def __contains__(self, item):
        if isinstance(item, Issue):
            return self.issue == item.identifier
        elif isinstance(item, IssueWorkItem):
            return item.identifier in self.work_items
        else:
            return NotImplemented

    def __iter__(self):
        return (self.__getitem_id(item) for item in self.work_items)

    def __getattribute__(self, item):
        if item in self.__slots__:
            return object.__getattribute__(self, item)
        return None

    def __len__(self):
        return len(self.work_items)

    def __setattr__(self, key, value):
        if key in self.__slots__:
            object.__setattr__(self, key, value)
        else:
            raise AttributeError(f"Incorrect attribute. Only {self.__slots__} are allowed.")

    def __getitem__(self, item):
        if item in self.work_items:
            return self.work_items[item]
        return None

    def __setitem__(self, key, value):
        self.work_items[key] = value

    @property
    def __get_issue(self) -> Issue:
        return ConstYT.dict_issue[self.issue]

    @property
    def state(self):
        return self.__get_issue.state

    @property
    def parent(self):
        return self.__get_issue.parent

    @property
    def summary(self):
        return self.__get_issue.summary

    @property
    def deadline(self):
        return self.__get_issue.deadline

    @property
    def commentary(self):
        return self.__get_issue.commentary

    @property
    def dates(self):
        return [self.__getitem_id(identifier).date for identifier in self.work_items]

    def __getitem_id(self, identifier: int) -> Optional[IssueWorkItem]:
        if identifier in self.work_items:
            return ConstYT.dict_issue_work_item[identifier]
        else:
            return None


def convert_timestamp(timestamp: str) -> Optional[str]:
    start_period = convert_date_iso(timestamp)
    return " .. ".join((start_period, "Today")) if start_period is not None else None


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


def post_request(url: str, headers: dict, params: tuple) -> str:
    """
    Defines the POST request.\n
    If the initial input parameters are invalid, the exception is raised.\n
    :param url: URL to send the request, str
    :param headers: request headers, dict
    :param params: request parameters, tuple
    :return: the response text of the str type. If the exception is raised, the empty string is returned.
    """
    try:
        response = requests.post(url=url, headers=headers, params=params)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f'The exception is {e.__class__}.')
        print('The request demands on the proper URL, headers, and params.')
        return '{}'


def convert_long_datetime(long) -> Optional[datetime.date]:
    """Converts the long value to the datetime.date."""
    if long is None:
        return None
    else:
        return datetime.date.fromtimestamp(numpy.divide(long, 1000))


def main():
    timestamp = check_terminate_script("Type the period start.")
    user = User()
    
    while user.login is None:
        if not user.verify_login:
            user = check_terminate_script("Print the login")
        else:
            break
    
    dict_issues = user.get_issues()


if __name__ == '__main__':
    main()
