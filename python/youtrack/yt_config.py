import datetime
import json
import pathlib
import os
from typing import Optional


class UserConfig:
    """
    Define the configuration file to initiate YouTrack requests.

    Constants:
        path --- the path to the JSON file, default: youtrack.json;\n
        default_period_start --- the start period date, default: the first day of the year;\n
        default_period_end --- the end period date, default: the current day;\n
        cell_attrs --- the attributes of the configuration file:\n
        (default "login", "auth_token", "period_start", "period_end");\n
        default_config --- the default values if the file does not exist;\n

    Functions:
        sys_login() --- get the system user from the OS environment;\n
        check_json(file_path) --- verify if the file exists;\n
        generate_json(file_path) --- create the file if does not exist;\n
        read_json(file_path) --- get the JSON file values;\n
        get_json_attr(key) --- get the JSON file attribute if exists;\n
        update_json_item(file_path, key, value) --- Modify the JSON file values;\n
        check_json_attrs(file_path) --- verify that all main values are specified;\n
        set_config_file(file_path) ---  the UserConfig instance parameter values;\n
    """
    path = pathlib.Path("./youtrack.json")

    today = datetime.date.today()
    date_period_start = datetime.date(today.year, 1, 1)
    default_period_start = date_period_start.strftime("%Y-%m-%d")
    default_period_end = today.strftime("%Y-%m-%d")
    # the names to replace
    __dict_name_conv: dict[str, str] = {"mozglyakova": "matyushina", "AndrewTarasov": "tarasov-a"}
    # the attributes
    attrs = ("login", "auth_token", "period_start", "period_end", "path_table")
    # the default configuration
    default_conf = {
        "login": "",
        "auth_token": "perm:dGFyYXNvdi1h.NjEtMTQw.1udDlV6zaAitHIgvw2eNQvF1sZ9JTZ",
        "period_start": f"{default_period_start}",
        "period_end": f"{default_period_end}",
        "path_table": "./report.xlsx"
    }
    # the configuration file parameters and values
    conf_values = dict()

    @staticmethod
    def sys_login() -> str:
        """
        Get the system user from the OS environment.

        :return: the name of the user.
        :rtype: str
        """
        if os.uname().sysname == "Windows":
            key = "USERNAME"
        else:
            key = "USER"
        sys_name = os.environ[key]
        return sys_name if sys_name not in UserConfig.__dict_name_conv else UserConfig.__dict_name_conv[sys_name]

    @staticmethod
    def check_json(file_path: pathlib.Path) -> bool:
        """
        Verify if the file exists.

        :param pathlib.Path file_path: the path to the file
        :return: the validation result.
        :rtype: bool
        """
        return file_path.exists()

    @staticmethod
    def generate_json(file_path: pathlib.Path):
        """
        Create the file if it does not exist.

        :param pathlib.Path file_path: the path to the file
        :return: None.
        """
        with open(file_path, "w") as json_file:
            json.dump(UserConfig.default_conf, json_file)

    @staticmethod
    def read_json(file_path: pathlib.Path) -> dict[str, str]:
        """
        Get the JSON file values.

        :param pathlib.Path file_path: the path to the file
        :return: the attribute dict values: login, auth_token, period_start, period_end, path_table.
        :rtype: dict[str, str]
        """
        with open(file_path, "r") as json_file:
            conf = json.load(json_file)
            for key, value in conf.items():
                UserConfig.conf_values[key] = value
        return UserConfig.conf_values

    @staticmethod
    def get_json_attr(key: str) -> Optional[str]:
        """
        Get the JSON file attribute if it exists.

        :param str key: the attribute key to get
        :return: the attribute value or None
        :rtype: str or None.
        """
        if key in UserConfig.conf_values.keys():
            return UserConfig.conf_values[key]
        else:
            print(f"AttributeError, the attribute {key} is not specified.")
            return None

    @staticmethod
    def update_json_item(file_path: pathlib.Path, key: str, value: str):
        """
        Modify the JSON file values.

        :param pathlib.Path file_path: the path to the file
        :param str key: the attribute name
        :param str value: the attribute value
        :return: None.
        """
        if key not in UserConfig.conf_values.keys():
            pass
        else:
            UserConfig.conf_values[key] = value
            with open(file_path, "w") as json_file:
                json.dump(UserConfig.conf_values.items(), json_file)

    @staticmethod
    def check_json_attrs(file_path: pathlib.Path):
        """
        Verify that all main values are specified.

        :param pathlib.Path file_path: the path to the file
        :return: None.
        """
        for key in UserConfig.attrs:
            if key not in UserConfig.conf_values.keys():
                UserConfig.conf_values[key] = UserConfig.default_conf[key]
            else:
                continue
        with open(file_path, "w") as json_file:
            json.dump(UserConfig.conf_values.items(), json_file)

    @staticmethod
    def set_config_file(file_path: pathlib.Path):
        """
        Define the UserConfig instance parameter values.

        :param pathlib.Path file_path: the path to file
        :return: the YouTrack configuration file.
        :rtype: UserConfig
        """
        if not UserConfig.check_json(file_path):
            UserConfig.generate_json(file_path)
        conf = UserConfig.read_json(file_path)
        for key, value in conf.items():
            UserConfig.conf_values[key] = value
        name = UserConfig.get_json_attr("login")
        print(f"name={name}")
        if not name or name in UserConfig.__dict_name_conv:
            login = UserConfig.sys_login()
            UserConfig.update_json_item(file_path, "login", login)
        UserConfig.check_json_attrs(file_path)
        user_config = UserConfig()
        return user_config


def main():
    pass


if __name__ == "__main__":
    main()
