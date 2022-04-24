import datetime
import json
import pathlib
import os
from typing import Optional


class UserConfig:
    """
    Define the configuration file to initiate YouTrack requests.
    
    Constants:
        path --- the path to the JSON configuration file (default "./youtrack.json")\n
        default_period_start --- the start period date (default the first day of the year)\n
        default_period_end --- the end period date (default the current day)\n
        attrs --- the attributes of the configuration file
        (default "login", "auth_token", "period_start", "period_end")\n
        default_config --- the default configuration file values if the file does not exist.\n

    Functions:
        func sys_login() -> str --- get the system name of the user\n
        check_json(file_path) -> bool -- verify if the file exists\n
        generate_json(file_path) --- generate the file is does not exist\n
        read_json(file_path) -> dict[str, str] --- get the JSON file dictionary\n
        get_json_attr(key) -> Optional[str] --- get the JSON file attribute if exists\n
        update_json_item(file_path, key, value) --- update the attribute value\n
        check_json_attrs(file_path) --- validate all required attributes are set, otherwise, add the default values\n
        set_config_file(file_path) --- initiate all steps to get the proper configuration file
    """

    path = pathlib.Path("./youtrack.json")

    today = datetime.date.today()
    date_period_start = datetime.date(today.year, 1, 1)
    default_period_start = date_period_start.strftime("%Y-%m-%d")
    default_period_end = today.strftime("%Y-%m-%d")

    __dict_name_conv: dict[str, str] = {"mozglyakova": "matyushina", "AndrewTarasov": "tarasov-a"}

    attrs = ("login", "auth_token", "period_start", "period_end")

    default_conf = {
        "login": "",
        "auth_token": "perm:dGFyYXNvdi1h.NjEtMTQw.1udDlV6zaAitHIgvw2eNQvF1sZ9JTZ",
        "period_start": f"{default_period_start}",
        "period_end": f"{default_period_end}"
    }

    conf_values = dict()

    @staticmethod
    def sys_login():
        if os.uname().sysname == "Windows":
            key = "USERNAME"
        else:
            key = "USER"
        sys_name = os.environ[key]
        return sys_name if sys_name not in UserConfig.__dict_name_conv else UserConfig.__dict_name_conv[sys_name]

    @staticmethod
    def check_json(file_path: pathlib.Path):
        return file_path.exists()

    @staticmethod
    def generate_json(file_path: pathlib.Path):
        with open(file_path, "w") as json_file:
            json.dump(UserConfig.default_conf, json_file)

    @staticmethod
    def read_json(file_path: pathlib.Path) -> dict[str, str]:
        with open(file_path, "r") as json_file:
            conf = json.load(json_file)
            for key, value in conf.items():
                UserConfig.conf_values[key] = value
        return UserConfig.conf_values

    @staticmethod
    def get_json_attr(key: str) -> Optional[str]:
        __doc__ = """
        Gets the Json file attribute if exists.
        
        :param key: the attribute key to get, str
        :return: the attribute value of the str type if the key is proper.
        """
        if key in UserConfig.conf_values:
            return UserConfig.conf_values[key]
        else:
            print("AttributeError, no such attribute.")
            return None

    @staticmethod
    def update_json_item(file_path: pathlib.Path, key: str, value: str):
        if key not in UserConfig.conf_values:
            pass
        else:
            UserConfig.conf_values[key] = value
            with open(file_path, "w") as json_file:
                json.dump(UserConfig.conf_values, json_file)

    @staticmethod
    def check_json_attrs(file_path: pathlib.Path):
        for key in UserConfig.attrs:
            if key not in UserConfig.conf_values:
                UserConfig.conf_values[key] = UserConfig.default_conf[key]
            else:
                continue
        with open(file_path, "w") as json_file:
            json.dump(UserConfig.conf_values, json_file)

    @staticmethod
    def set_config_file(file_path: pathlib.Path):
        if not UserConfig.check_json(file_path):
            UserConfig.generate_json(file_path)
        conf = UserConfig.read_json(file_path)
        for key, value in conf.items():
            UserConfig.conf_values[key] = value
        name = UserConfig.get_json_attr("login")
        if not name or name in UserConfig.__dict_name_conv:
            login = UserConfig.sys_login()
            UserConfig.update_json_item(file_path, "login", login)
        UserConfig.check_json_attrs(file_path)


def main():
    UserConfig.set_config_file(UserConfig.path)


if __name__ == "__main__":
    main()
