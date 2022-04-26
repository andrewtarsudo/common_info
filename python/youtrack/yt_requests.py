import pathlib
import pprint
from json.decoder import JSONDecodeError
from typing import Union, Optional
import numpy
from requests.exceptions import RequestException, HTTPError, ConnectionError, InvalidURL, InvalidHeader
import requests
import datetime
import re
from yt_config import UserConfig


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

    date_conversion_rules = (
        (re.compile(r'(\d{4}).(\d{1,2}).(\d{1,2})'), (1, 2, 3)),
        (re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})'), (3, 2, 1))
    )


def check_terminate_script(prompt: str) -> str:
    """
    Check the input to terminate the program.

    :param str prompt: the text to display
    :type prompt: str
    :return: either exit() or modified command
    :rtype: str
    """
    user_input = input(prompt)
    # delete trailing zeros and lower case
    user_command = user_input.lower().strip()

    if user_command == "__exit__":
        print('Работа прервана. Программа закрывается.')
        exit()
    else:
        return user_command


def make_request(method: str, url: str, headers, params) -> Union[list, Optional[dict]]:
    """
    Combines and sends the request.\n
    If the request is improper, prints the error.\n
    Method values: GET/POST/PUT/DELETE/HEAD/OPTIONS

    :param str method: the HTTP request type
    :param str url: the destination URL
    :param headers: the HTTP headers
    :type headers: dict[str, str] or dict[str, dict]
    :param tuple[tuple[str, str]] params: the HTTP parameters
    :return: the response text or the JSON-converted object
    :rtype: list or dict[str, str] or dict[str, dict] or None
    """
    try:
        response = requests.request(method=method, url=url, headers=headers, params=params).json()
    except InvalidURL as e:
        print(f"InvalidURL {e.errno}, {e.strerror}. Incorrect request URL.")
        return None
    except InvalidHeader as e:
        print(f"Invalid Header {e.errno}, {e.strerror}. Incorrect headers.")
        return None
    except ConnectionError as e:
        print(f"ConnectionError {e.errno}, {e.strerror}. Connection failed.")
        return None
    except HTTPError as e:
        print(f"HTTPError {e.errno}, {e.strerror}. Main HTTP request error")
        return None
    except RequestException as e:
        print(f"RequestError {e.errno}, {e.strerror}. Main request error.")
        return None
    except OSError as e:
        print(f"OSError {e.errno}, {e.strerror}. Global error occurred.")
        return None
    except JSONDecodeError as e:
        print(f"JSONDecodeError {e.msg}. Response cannot be parsed as JSON data.")
        return None
    else:
        return response


def convert_date_iso(input_date: str) -> Optional[datetime.date]:
    """
    Converts different date formats to the ISO standard.

    :param str input_date: the date to convert
    :return: the modified date of the str type.
    """

    for pattern, group_match in ConstYT.date_conversion_rules:
        match = re.match(pattern, input_date)
        # find the pattern to convert
        if match:
            i_1, i_2, i_3 = group_match
            date_iso = f'{match.group(i_1)}-{match.group(i_2)}-{match.group(i_3)}'
            return datetime.date.fromisoformat(date_iso)
        else:
            continue
    return None


def define_deadline_state(issue_name: str, res: str) -> Optional[str]:
    """
    Define the deadline and state identifier based on the issue name.

    res values: deadline/state\n
    :param str issue_name: the name of the issue
    :param str res: the required identifier
    :return: the parameter identifier of the str type
    :rtype: str or None
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
    __slots__ = "user_config"

    def __init__(self, user_config: UserConfig):
        self.user_config = user_config

    def __str__(self):
        return f"User: config file {self.user_config.path}"

    def __repr__(self):
        return f"User(user_config={self.user_config})"

    @property
    def login(self):
        """Shorten the login call."""
        return self.user_config.get_json_attr("login")

    @property
    def period_start(self):
        """Shorten the period_start call."""
        return self.user_config.get_json_attr("period_start")

    @property
    def period_end(self):
        """Shorten the period_end call."""
        return self.user_config.get_json_attr("period_end")

    @property
    def auth_token(self):
        """Shorten the auth_token call."""
        return self.user_config.get_json_attr("auth_token")

    @property
    def get_login(self) -> str:
        """Get the login to authorize in the YouTrack."""
        if not self._verify_login(self.login):
            login = self.__login_input
            self.user_config.update_json_item(UserConfig.path, "login", login)
        return self.login

    @property
    def __headers_yt(self) -> dict[str, str]:
        """Set the headers for requests."""
        bearer = " ".join(("Bearer", self.auth_token))
        return {
            "Authorization": bearer,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def request(self, url: str, params: tuple, method: str = "get"):
        """Shorten the request sending."""
        return make_request(method, url, self.__headers_yt, params)

    def _verify_login(self, login_option: str) -> bool:
        """
        Check if the login_option is a proper login.

        :param str login_option: the login to try
        :return: the flag if the "error" key is in the response
        :rtype: bool
        """
        url = f"https://youtrack.protei.ru/api/users/{login_option}"
        params = (('fields', 'login'),)
        return "error" not in self.request(url, params).keys()

    @property
    def __login_input(self):
        """Get the login from the user input."""
        # if the login is correct
        if self._verify_login(self.login):
            return self.login
        # if the login is incorrect
        else:
            while True:
                login_input = check_terminate_script("Print the login.\n")
                if self._verify_login(login_input):
                    return login_input
                else:
                    continue

    @property
    def period(self) -> str:
        """Set the period to get the issues and work items."""
        # convert the date inputs
        start = convert_date_iso(self.period_start)
        end = convert_date_iso(self.period_end)
        # convert the start and end dates to the period string
        start_period = start.strftime("%Y-%m-%d")
        end_period = end.strftime("%Y-%m-%d")
        return " .. ".join((start_period, end_period))

    def get_issue_work_items(self):
        """Gets the work issues: name, date, spent_time."""
        # define the parameters of the request
        url = 'https://youtrack.protei.ru/api/workItems'
        parameters_fields = ','.join(('duration(minutes)', 'date', 'issue(idReadable)'))
        parameters_query = ' '.join((f'work author: {self.login}', f'work date: {self.period}'))
        params = (
            ('fields', parameters_fields),
            ('query', parameters_query),
        )
        # get the response in the JSON format
        parsed_response = self.request(url, params)
        for item in parsed_response:
            issue, date, modified_spent_time = parse_response_work_item(item)
            IssueWorkItem(issue, date, modified_spent_time)

    def get_issues(self):
        """Get issues with the period defined."""
        # define the parameters of the request
        states_period = "state: Done, Test, Verified, Closed, Canceled, Review"
        states_no_period = "state: New, Active, Paused, Discuss"
        url = 'https://youtrack.protei.ru/api/issues'
        parameters_fields = ','.join(('idReadable', 'summary', 'parent(issues(idReadable))'))
        parameters_query_period = ' '.join((f'assignee: {self.login}', f'updated: {self.period}', states_period))
        parameters_query_no_period = ' '.join((f'assignee: {self.login}', states_no_period))
        params_period = (
            ('fields', parameters_fields),
            ('query', parameters_query_period),
        )
        params_no_period = (
            ('fields', parameters_fields),
            ('query', parameters_query_no_period),
        )
        # get the response in the JSON format
        parsed_response_period = self.request(url, params_period)
        parsed_response_no_period = self.request(url, params_no_period)
        parsed_response = [*parsed_response_period, *parsed_response_no_period]
        # define the parameters of the issue
        for item in parsed_response:
            self.parse_response_issue(item)

    def get_issue_state(self, issue: str) -> Optional[str]:
        """
        Defines the state of the issue from the YouTrack.\n
        :param issue: the issue identifier, idReadable, str
        :return: the issue state of the str type.
        """
        state_identifier = define_deadline_state(issue, 'state')

        if state_identifier is None:
            return None
        else:
            # define the parameters of the request
            url = f'https://youtrack.protei.ru/api/issues/{issue}/customFields/{state_identifier}'
            params = (('fields', 'value(name)'),)
            # get the response in the JSON format
            parsed_response = self.request(url, params)

            if "value" in parsed_response.keys() and "name" in parsed_response["value"].keys():
                return convert_issue_state(parsed_response['value']['name'])
            else:
                return None

    def get_issue_deadline(self, issue: str) -> datetime.date:
        """
        Defines the deadline of the issue from the YouTrack.

        :param str issue: the issue identifier, idReadable
        :return: the issue deadline.
        :rtype: date
        """
        deadline_identifier = define_deadline_state(issue, 'deadline')
        deadline: datetime.date = datetime.date(1, 1, 1)
        if deadline_identifier != 'None':
            # define the parameters of the request
            url = f'https://youtrack.protei.ru/api/issues/{issue}/customFields/{deadline_identifier}'
            params = (('fields', 'value(name)'),)
            # get the response in the JSON format
            parsed_response = self.request(url, params)

            if "value" in parsed_response.keys():
                deadline = convert_long_date(parsed_response['value'])
        return deadline

    def get_issue_id(self, issue: str):
        """
        Defines the dict of the issue parameters: parent, name, summary, deadline, state, work_items.

        :param str issue: the issue name, str
        """
        # define the parameters of the request
        url = f'https://youtrack.protei.ru/api/issues/{issue}'
        parameters_fields = ','.join(('idReadable', 'summary', 'parent(issues(idReadable))'))
        params = (('fields', parameters_fields),)
        # get the response in the JSON format
        parsed_response = self.request(url, params)
        self.parse_response_issue(parsed_response)

    def parse_response_issue(self, response_item: dict):
        """

        :param response_item:
        :return:
        """
        # define the issue name
        issue: str = response_item['idReadable']
        # define the parent issue name
        parent_issues = response_item['parent']['issues']
        parent: Optional[str]
        # check if the parent issue __exists
        if len(parent_issues):
            parent = parent_issues[0]['idReadable']
        else:
            parent = None
        # define the issue summary
        summary: str = response_item['summary']
        # define the issue deadline
        deadline: datetime.date = self.get_issue_deadline(issue)
        # define the issue state
        state = self.get_issue_state(issue)
        Issue(issue, state, summary, parent, deadline)


def convert_long_date(long) -> Optional[datetime.date]:
    """
    Convert the long value to the date.

    :param long: the timestamp
    :return: the date associated with the timestamp
    :rtype: date or None
    """
    if long is None:
        return None
    else:
        return datetime.date.fromtimestamp(numpy.divide(long, 1000))


def convert_spent_time(spent_time: int) -> Union[int, float]:
    """
    Convert the spent time in minutes to hours.

    :param int spent_time: the spent time in minutes
    :return: the converted spent time in hours
    :rtype: int or float
    """
    return numpy.divide(spent_time, 60)


def parse_response_work_item(response_item: dict):
    """
    Get the parameters from the response item.

    :param dict response_item: the item from the response
    :return: the issue name, date, and modified spent time.
    :rtype: tuple[str, datetime.date, Union[int, float]]
    """
    # define the issue name of the work item
    issue: str = response_item['issue']['idReadable']
    # define the date of the work item
    date: datetime.date = convert_long_date(response_item['date'])
    # define the spent time of the work item
    spent_time: int = response_item['duration']['minutes']
    # convert to the hours
    modified_spent_time: Union[int, float] = convert_spent_time(spent_time)
    return issue, date, modified_spent_time


def convert_issue_state(state: str) -> str:
    """
    Converts the state to the table headers.\n
    :param state: the issue state, str
    :return: the modified state of the str type.
    """
    # the issues to convert to the New/Paused
    to_new_paused = ('New', 'Paused', 'Canceled', 'Discuss')
    # the issues to convert to the Done/Test
    to_done_test = ('Done', 'Test', 'Review')
    # the issues to convert to the Verified
    to_verified = ('Closed',)

    if state in to_new_paused:
        modified_state = 'New/Paused'
    elif state in to_done_test:
        modified_state = 'Done/Test'
    elif state in to_verified:
        modified_state = 'Verified'
    else:
        print(f"Unspecified state {state} is found.")
        modified_state = state
    return modified_state


class Issue:
    """Define the Issue entity from the YouTrack.

    Params:
        index --- the unique issue identifier, 0-based\n
        issue --- the issue name, idReadable, {project}-{id}\n
        state --- the issue state, state
        summary -- the issue short description, summary
        parent --- the parent issue name, parent
        deadline --- the issue deadline, deadline

    state values: Active/New/Paused/Done/Test/Verified/Discuss/Closed/Review/Canceled\n
    """
    index = 0

    __slots__ = ("identifier", "issue", "state", "summary", "parent", "deadline")

    def __init__(
            self,
            issue: str,
            state: str,
            summary: str,
            parent: str = None,
            deadline: datetime.date = None):
        self.identifier = Issue.index
        self.issue = issue
        self.state = state
        self.summary = summary
        self.parent = parent
        self.deadline = deadline

        ConstYT.dict_issue[self.issue] = self
        Issue.index += 1

    def __str__(self):
        str_parent = ""
        str_deadline = ""
        if self.parent is not None:
            str_parent = f", parent = {self.parent}"
        if self.deadline is not None:
            str_deadline = f", deadline = {self.deadline.strftime('%d.%m.%Y')}"

        return f"Issue: name = {self.issue}, state = {self.state}, summary = {self.summary}{str_parent}{str_deadline}"

    def __repr__(self):
        return f"Issue(name={self.issue}, state={self.state}, summary={self.summary}, parent={self.parent}, " \
               f"deadline={self.deadline})"

    def __hash__(self):
        return hash((self.identifier, self.issue, self.state))

    def __key(self):
        return self.identifier, self.issue, self.state

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


class IssueWorkItem:
    index = 0

    __slots__ = ("identifier", "issue", "date", "spent_time")

    def __init__(self, issue: str, date: datetime.date, spent_time: int):
        self.identifier = IssueWorkItem.index
        self.issue = issue
        self.date = date
        self.spent_time = spent_time

        ConstYT.dict_issue_work_item[self.identifier] = self
        IssueWorkItem.index += 1

    def __str__(self):
        return f"IssueWorkItem: issue = {self.issue}, date = {self.date}, spent time = {self.spent_time}"

    def __repr__(self):
        return f"IssueWorkItem(issue={self.issue}, date={self.date}, spent_time={self.spent_time})"

    def __hash__(self):
        return hash((self.identifier, self.issue, self.date, self.spent_time))

    def __key_eq(self):
        return self.identifier, self.issue, self.date, self.spent_time

    def __eq__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.__key_eq() == other.__key_eq()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, IssueWorkItem):
            return self.__key_eq() != other.__key_eq()
        else:
            return NotImplemented

    def __key_order(self):
        return self.issue, self.date

    def __join_items(self, other):
        """Combines the work items with the same issue and date into the single one."""
        if isinstance(other, IssueWorkItem):
            if self.__key_order() == other.__key_order() and self.spent_time != other.spent_time:
                IssueWorkItem(self.issue, self.date, self.spent_time + other.spent_time)
                del other
                del self

    def __lt__(self, other):
        if isinstance(other, IssueWorkItem) and self.issue == other.issue:
            return self.date < other.date
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, IssueWorkItem) and self.issue == other.issue:
            return self.date > other.date
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, IssueWorkItem) and self.issue == other.issue:
            return self.date <= other.date
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, IssueWorkItem) and self.issue == other.issue:
            return self.date >= other.date
        else:
            return NotImplemented


class _IssueMerged:
    index = 0

    def __init__(self, issue_name: str):
        self.issue_name = issue_name

    def __hash__(self):
        return hash(self.issue_name)

    def __key(self):
        return self.issue_name, self.issue_item, self.work_items

    def __eq__(self, other):
        if isinstance(other, _IssueMerged):
            return self.issue_name == other.issue_name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _IssueMerged):
            return self.__key() != other.issue_name
        else:
            return NotImplemented

    def __len__(self):
        return len(self.work_items)

    def __contains__(self, item):
        if isinstance(item, Issue):
            return self.issue_item == item
        elif isinstance(item, IssueWorkItem):
            return item in self.work_items
        else:
            return NotImplemented

    def __getitem__(self, item):
        if item < len(self.work_items):
            return self.work_items[item]
        else:
            return None

    def __setitem__(self, key, value):
        self.work_items[key] = value

    def __iter__(self):
        return (work_item for work_item in self.work_items)

    @property
    def issue_item(self):
        issue: Issue
        for issue in ConstYT.dict_issue.values():
            if issue.issue == self.issue_name:
                return issue

    @property
    def work_items(self):
        work_item: IssueWorkItem
        return [work_item for work_item in ConstYT.dict_issue_work_item.values() if work_item.issue == self.issue_name]


def main():
    path = pathlib.Path("./youtrack.json")
    user_config = UserConfig.set_config_file(path)
    user = User(user_config)
    url = 'https://youtrack.protei.ru/api/issues'
    parameters_fields = ','.join(('project', 'id', 'idReadable'))
    parameters_query = ' '.join((f'updater: {user.login}', f'assignee: {user.login}'))
    params = (
        ('fields', parameters_fields),
        ('query', parameters_query),
    )
    response = user.request(url, params)
    pprint.pprint(response)
    print(len(response))
    print(type(response))


if __name__ == "__main__":
    main()
