from decimal import Decimal
from json.decoder import JSONDecodeError
from typing import Union, Optional
import numpy
from requests.exceptions import RequestException, HTTPError, ConnectionError, InvalidURL, InvalidHeader
import requests
import datetime
import re
from yt_config import UserConfig
from collections import Counter


class ConstYT:
    """
    Contain the constants.

    Constants:\n
        date_conversion_rules --- the rules to convert the user input dates;
    """
    # patterns to parse user-defined period dates
    date_conversion_rules = (
        (re.compile(r'(\d{4}).(\d{1,2}).(\d{1,2})'), (1, 2, 3)),
        (re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})'), (3, 2, 1))
    )


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
    Combine and send the request.\n
    If the request is improper, print the error.\n
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
    Convert different date formats to the ISO standard.

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


def parse_response_work_item(response_item: dict) -> tuple[str, datetime.date, Decimal]:
    """
    Get the parameters from the response item.

    :param dict response_item: the item from the response
    :return: the issue name, date, and modified spent time.
    :rtype: tuple[str, date, Decimal]
    """
    # define the issue name of the work item
    issue: str = response_item['issue']['idReadable']
    # define the date of the work item
    date: datetime.date = convert_long_date(response_item['date'])
    # define the spent time of the work item
    spent_time: int = response_item['duration']['minutes']
    # convert to the hours
    modified_spent_time: Union[int, float] = convert_spent_time(spent_time)
    return issue, date, Decimal(modified_spent_time).normalize()


def parse_response_issue(response_item: dict):
    """
    Parse the response in the dict format to get Issue.

    :param response_item: the response to parse
    :type response_item: dict[str, Union[str, dict]]
    :return: None.
    """
    # define the issue name
    issue: str = response_item['idReadable']
    # define the parent issue name
    parent_issues = response_item['parent']['issues']
    parent: Optional[str]
    # check if the parent issue exists
    if len(parent_issues):
        parent = parent_issues[0]['idReadable']
    else:
        parent = None
    # define the issue summary
    summary: str = response_item['summary']
    deadline: datetime.date = datetime.date(1, 1, 1)
    state: str = ""
    for item in response_item["customFields"]:
        # define the issue state
        if item["$type"] == "StateIssueCustomField":
            state = item["value"]["name"]
        # define the issue deadline
        elif item["$type"] == "DateIssueCustomField":
            deadline = convert_long_date(item["value"])
        else:
            continue
    return issue, state, summary, parent, deadline


class User:
    """
    Define the User entity to send the YouTrack requests.

    Params:
        user_config --- the UserConfig item;\n
        dict_issue --- the dictionary of Issue instances and identifiers;\n
        dict_issue_work_item --- the dictionary of IssueWorkItem instances and identifiers;\n

    Properties:
        login --- the login call;\n
        period_start --- the period_start call;\n
        period_end --- the period_end call;\n
        __headers_yt --- the headers for requests;\n
        start_period --- the start period of the specified format;\n
        end_period --- the end period of the specified format;\n
        period --- the period of the specified format;\n
        path_table --- the path to the report;\n
        _get_non_unique --- the non-unique work items;\n

    Functions:
        auth_token() --- get the auth_token;\n
        request(url, params, method: default="get") --- send the request;\n
        _verify_login(login_option) --- verify if the login_option is a proper login;\n
        login_input() --- get the login from the user input;\n
        get_issue_work_items() --- get the IssueWorkItem instances;\n
        get_issues() --- get the Issue instances;\n
        get_current_issues() --- get the Issue instances with no work items;\n
        issues_from_yt() --- get all issue information from the YouTrack;\n
        _join_work_items() --- combine the non-unique work items;\n
    """

    def __init__(self, user_config: UserConfig):
        self.user_config = user_config
        self.dict_issue = dict()
        self.dict_issue_work_item = dict()

    def __str__(self):
        return f"User: config file {self.user_config.path}, login; {self.login}"

    def __repr__(self):
        return f"User(user_config={self.user_config.conf_values})"

    @property
    def login(self) -> str:
        """
        Shorten the login call.

        :return: the login.
        :rtype: str
        """
        return self.user_config.get_json_attr("login")

    @property
    def period_start(self) -> str:
        """
        Shorten the period_start call.

        :return: the period_start.
        :rtype: str
        """
        return self.user_config.get_json_attr("period_start")

    @property
    def period_end(self) -> str:
        """
        Shorten the period_end call.

        :return: the period_end.
        :rtype: str
        """
        return self.user_config.get_json_attr("period_end")

    def auth_token(self) -> str:
        """
        Shorten the auth_token call.

        :return: the auth_token.
        :rtype: str
        """
        return self.user_config.get_json_attr("auth_token")

    @property
    def path_table(self):
        """
        Shorten the path_table call.

        :return: the path to the report.
        :rtype: str
        """
        return self.user_config.get_json_attr("path_table")

    @property
    def __headers_yt(self) -> dict[str, str]:
        """
        Set the headers for requests.

        :return: the headers.
        :rtype: dict[str, str]
        """
        bearer = " ".join(("Bearer", self.auth_token))
        return {
            "Authorization": bearer,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def request(self, url: str, params: tuple, method: str = "get"):
        """
        Shorten the request sending.

        :param str url: the request URL
        :param tuple params: the HTTP request parameters
        :param str method: the HTTP method, default "get"
        :return: the request response.
        """
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

    def login_input(self) -> str:
        """
        Get the login from the user input.

        :return: the user input.
        :rtype: str
        """
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
    def start_period(self) -> str:
        """
        Get the start period of the specified format.

        :return: the start date.
        :rtype: str
        """
        return convert_date_iso(self.period_start).strftime("%Y-%m-%d")

    @property
    def end_period(self) -> str:
        """
        Get the end period of the specified format.

        :return: the end date.
        :rtype: str
        """
        return convert_date_iso(self.period_end).strftime("%Y-%m-%d")

    @property
    def period(self) -> str:
        """
        Set the period to get the issues and work items.

        :return: the period.
        :rtype: str
        """
        return " .. ".join((self.start_period, self.end_period))

    def get_issue_work_items(self):
        """Get the IssueWorkItem instances."""
        # define the parameters of the request
        url = 'https://youtrack.protei.ru/api/workItems'
        parameters_fields = ','.join(('duration(minutes)', 'date', 'issue(idReadable)'))
        parameters_query = ' '.join((f'work author: {self.login}', f'work date: {self.period}'))
        parameters_start_date = self.start_period
        parameters_end_date = self.end_period
        parameters_author = self.login
        params = (
            ('fields', parameters_fields),
            ('query', parameters_query),
            ('startDate', parameters_start_date),
            ('endDate', parameters_end_date),
            ('author', parameters_author)
        )
        # get the response in the JSON format
        parsed_response = self.request(url, params)
        for item in parsed_response:
            issue, date, modified_spent_time = parse_response_work_item(item)
            IssueWorkItem(self, issue, date, modified_spent_time)

    def get_issues(self):
        """Get the Issue instances."""
        issue_names = ",".join([issue_name for issue_name in list(self.dict_issue_work_item.values())])
        url = 'https://youtrack.protei.ru/api/issues'
        parameters_fields = ','.join(('idReadable', 'summary', "parent(issues(idReadable))",
                                      'customFields(value,value(name),projectCustomField(field(name)))'))
        parameters_query = " ".join((f'issue ID: {issue_names}', f'updated: {self.period}'))
        parameters_custom_fields_state = "State"
        parameters_custom_fields_deadline = "Дедлайн"
        params = (
            ('fields', parameters_fields),
            ('query', parameters_query),
            ('customFields', parameters_custom_fields_state),
            ('customFields', parameters_custom_fields_deadline),
        )
        # get the response in the JSON format
        parsed_response = self.request(url, params)
        for item in parsed_response:
            issue, state, summary, parent, deadline = parse_response_issue(item)
            Issue(self, issue, state, summary, parent, deadline)

    def get_current_issues(self):
        """Get the non-closed Issue instances with no IssueWorkItem instances."""
        states = ",".join(("New", "Active", "Discuss", "Paused"))
        url = 'https://youtrack.protei.ru/api/issues'
        parameters_fields = ','.join(('idReadable', 'summary', "parent(issues(idReadable))",
                                      'customFields(value,value(name),projectCustomField(field(name)))'))
        parameters_query = " ".join((f'State: {states}', f'Assignee: {self.login}'))
        parameters_custom_fields_state = "State"
        parameters_custom_fields_deadline = "Дедлайн"
        params = (
            ('fields', parameters_fields),
            ('query', parameters_query),
            ('customFields', parameters_custom_fields_state),
            ('customFields', parameters_custom_fields_deadline),
        )
        # get the response in the JSON format
        parsed_response = self.request(url, params)
        for item in parsed_response:
            issue, state, summary, parent, deadline = parse_response_issue(item)
            Issue(self, issue, state, summary, parent, deadline)

    def issue_names(self) -> list[str]:
        """
        Get the issue names.

        :return: the issue names.
        :rtype: list[str]
        """
        return list(self.dict_issue.keys())

    def issues_from_yt(self):
        """Get all YouTrack information."""
        self.get_issue_work_items()
        self.get_issues()
        self.get_current_issues()
        self._join_work_items()

    @property
    def __non_unique(self) -> dict[str, list[datetime.date]]:
        """
        Get the non-unique work items.

        :return: the dictionary of the issue names and dates.
        :rtype: dict[str, list[date]]
        """
        non_unique: dict[str, list[datetime.date]] = dict()
        issue_name: str
        for issue_name, work_items in self.dict_issue_work_item.items():
            counter = Counter([work_item.date for work_item in work_items])
            non_unique_date = [key for key, value in counter.items() if value > 1]
            if not len(non_unique_date):
                non_unique[issue_name] = non_unique_date
        return non_unique

    def _join_work_items(self):
        """Join the non-unique work items."""
        for issue, dates in self.__non_unique.items():
            for date in dates:
                work_item: IssueWorkItem
                # cumulative sum
                cum_spent_time = numpy.cumsum(
                    [work_item.spent_time for work_item in self.dict_issue_work_item.values()
                     if work_item.issue == issue and work_item.date == date])
                # delete
                del_work_items = [
                    work_item for work_item in self.dict_issue_work_item.values()
                    if work_item.issue == issue and work_item.date == date]
                for item in del_work_items:
                    del item
                IssueWorkItem(self, issue, date, cum_spent_time)


class Issue:
    """
    Define the Issue entity from the YouTrack.

    Class params:
        attrs --- the attributes:\n
        "issue", "state", "summary", "parent", "deadline";\n

    Params:
        user --- the user instance;\n
        issue --- the issue name, idReadable, {project}-{id};\n
        state --- the issue state, state;\n
        summary -- the issue short description, summary;\n
        parent --- the parent issue name, parent;\n
        deadline --- the issue deadline, deadline;\n

    state values:\n
    Active/New/Paused/Done/Test/Verified/Discuss/Closed/Review/Canceled\n

    Functions:
        to_tuple() --- represent the instance as a tuple;\n
    """
    attrs = ("issue", "state", "summary", "parent", "deadline")

    __slots__ = ("user", "issue", "state", "summary", "parent", "deadline")

    def __init__(
            self,
            user: User,
            issue: str,
            state: str,
            summary: str,
            parent: str = None,
            deadline: datetime.date = None):
        self.user = user
        self.issue = issue
        self.summary = summary
        self.parent = parent
        if deadline == datetime.date(1, 1, 1):
            self.deadline = None
        else:
            self.deadline = deadline
        if state == "":
            self.state = None
        else:
            self.state = state

        self.user.dict_issue[self.issue] = self

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
        return hash((self.issue, self.state))

    def __key(self):
        return self.issue, self.state

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

    def to_tuple(self):
        """
        Represent the instance as a tuple.

        :return: the tuple of the issue attributes.
        :rtype: tuple[str, str, str, str or None, datetime.date or None]
        """
        return tuple(getattr(self, attr) for attr in Issue.attrs)


class IssueWorkItem:
    """
    Define the IssueWorkItem entity from the YouTrack.

    Class params:
        attrs --- the attributes: "issue", "date", "spent_time";\n

    Params:
        issue --- the issue name, idReadable, {project}-{id};\n
        date --- the issue work item date, date;\n
        spent_time -- the issue work item recorded time in minutes, int;\n

    state values:\n
    Active/New/Paused/Done/Test/Verified/Discuss/Closed/Review/Canceled\n

    Functions:
        to_tuple() --- represent the instance as a tuple;\n
    """
    attrs = ("issue", "date", "spent_time")

    __slots__ = ("user", "issue", "date", "spent_time")

    def __init__(
            self,
            user: User,
            issue: str,
            date: datetime.date,
            spent_time: Decimal):
        self.user = user
        self.issue = issue
        self.date = date
        self.spent_time = Decimal(spent_time).normalize()

        self.user.dict_issue_work_item[self.issue] = self

    def __str__(self):
        return f"IssueWorkItem: issue = {self.issue}, date = {self.date}, spent time = {self.spent_time}"

    def __repr__(self):
        return f"IssueWorkItem(issue={self.issue}, date={self.date}, spent_time={self.spent_time})"

    def __hash__(self):
        return hash((self.issue, self.date, self.spent_time))

    def __key_eq(self):
        return self.issue, self.date, self.spent_time

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

    def to_tuple(self):
        """
        Represent the instance as a tuple.

        :return: the tuple of the issue work item attributes.
        :rtype: tuple[str, datetime.date, Decimal]
        """
        return tuple(getattr(self, attr) for attr in IssueWorkItem.attrs)


def main():
    pass


if __name__ == "__main__":
    main()
