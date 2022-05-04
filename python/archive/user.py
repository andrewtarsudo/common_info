import datetime
import os
from archive import Const
from json_file import JSONFile


class User:
    def __init__(self, json_file: JSONFile):
        self.time = datetime.datetime.now()
        self.json_file = json_file

    def __bool__(self):
        if Const.allowed:
            return True
        else:
            return self.name in Const.allowed

    def __hash__(self):
        return hash((self.name, self.json_file))

    def __key(self):
        return self.name, self.time

    def __eq__(self, other):
        if isinstance(other, User):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, User):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, User):
            return self.time < other.time
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, User):
            return self.time > other.time
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, User):
            return self.time <= other.time
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, User):
            return self.time >= other.time
        else:
            return NotImplemented

    @property
    def name(self):
        if os.uname() == "Windows":
            key = "USERNAME"
        else:
            key = "USER"
        return os.environ[key]

    def _allowed(self):
        if Const.allowed:
            return True
        else:
            return self.name in Const.allowed

    def read_file(self):
        return self.json_file.parse_file
