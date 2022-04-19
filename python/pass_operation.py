import os
import pathlib
import platform
import hashlib
from typing import Union


class PasswordList:
    def __init__(self, name: str, pass_list: list = None):
        if pass_list is None:
            pass_list = []

        self.name = name
        self.pass_list = pass_list

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, PasswordList):
            return self.name == other.name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, PasswordList):
            return self.name != other.name
        else:
            return NotImplemented

    def __contains__(self, item):
        return item in self.pass_list


class Password:
    def __init__(self, password: str, resource: str, algorithm: str, mail: str = None, nick_name: str = None,
                 important: bool = False):
        self.password = password
        self.resource = resource
        self.algorithm = algorithm
        self.mail = mail
        self.nick_name = nick_name
        self._important = important

    def __key(self):
        return self.password, self.resource, self._important

    def __str__(self):
        if self._safety:
            return f"Password {self.password} for the resource {self.resource}.\n" \
                   f"Mail: {self.mail}, nickname: {self.nick_name}"
        else:
            return "Password ___ for the resource ___.\nMail: ___, nickname: ___"

    def __repr__(self):
        if self._safety:
            return f"Password(password={self.password}, resource={self.resource}, mail={self.mail}, " \
                   f"nick_name={self.nick_name}, important={self._important})"
        else:
            return "Password(password=___, resource=___, mail=___, nick_name=___, important=___"

    def __hash__(self):
        return hash((self.password, self.resource, self._important))

    def __eq__(self, other):
        if isinstance(other, Password):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Password):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __bool__(self):
        return self._important

    @property
    def _safety(self):
        return bool(self) and self._sys_login is not None

    @property
    def _sys_login(self):
        if platform.system() == "Darwin":
            return os.environ.get("USERNAME")
        elif platform.system() == "Windows":
            return os.environ.get("USER")
        else:
            return None

    @property
    def _sys_name(self):
        if self._sys_login is None:
            return None
        else:
            return hashlib.sha256(bytes(self._sys_login, encoding="ascii"))

    @property
    def __checksum(self):
        return "1d7abb4d89c8c1c399d470b07354a5ff34b963215634637a13c34f8c86e2eecd"

    def __check_file(self, path: Union[str, pathlib.Path]):
        try:
            hash_checksum = hashlib.new(self.algorithm)
            with open(path, "rb") as file:
                # cut the file into the pieces of the 4096 bits
                for chunk in iter(lambda: file.read(4096), b""):
                    hash_checksum.update(chunk)

        except FileNotFoundError as e:
            print(f"The FileNotFoundError {e.errno}, {e.strerror}.")
            return False
        except IsADirectoryError as e:
            print(f"The IsADirectoryError {e.errno}, {e.strerror}.")
            return False
        except PermissionError as e:
            print(f"The PermissionError {e.errno}, {e.strerror}.")
            return False
        except OSError as e:
            print(f"The OSError {e.errno}, {e.strerror}.")
            return False
        else:
            return hash_checksum.hexdigest() == self.__checksum

    @property
    def salt(self):
        hash_result = hashlib.new("sha256")
        if self._safety:
            salt_string = "_".join((self.password, self.resource, self._sys_name))
        else:
            salt_string = "_".join((self.password, self.resource))
        byte_salt = bytes(salt_string, encoding="ascii")
        hash_result.update(byte_salt)

        return hash_result.hexdigest()


class _Encrypted:
    def __init__(self, file_json: str, password: Password):
        self.file_json = file_json
        self._password = password

    def __key(self):
        hash_sum = hashlib.new(self._password.algorithm)
        hash_sum.update(self._password.password)
        return hash_sum.hexdigest(), self._password.resource, self._password.mail, self._password.nick_name

    @property
    def algorithm(self):
        return self._password.algorithm

    @property
    def password_clear(self):
        return self._password.password

    def salt(self):
        return self._password.salt

    @property
    def __checksum(self):
        hash_sum = hashlib.new(self.algorithm)
        hash_sum.update(self._password.password)
        return hash_sum.hexdigest()

    def __contains__(self, item):
        if isinstance(item, tuple) and len(item) == 2:
            password, resource = item
            if self.password_clear == password and self._password.resource == resource:
                return True
            return False
        return False
                
            

