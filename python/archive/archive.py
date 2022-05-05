import datetime
from pathlib import Path
import os
from copy import copy
from pprint import pprint
from typing import Optional, Union
import logging
import json
from json import JSONDecodeError
from hashlib import md5

filename = "./basic_log.log"
fmt = "%(levelName)s %(asctime)s, %(funcName) --- %(message)s"
level = logging.INFO
logging.basicConfig(filename=filename, format=fmt, level=level)


class Const:
    dict_file = dict()

    list_doc_types = [""]
    list_cabinet_names = [""]
    list_shelf_no = [1, 2, 3]
    list_folder_names = [""]

    yes_answers = ("y", "yes", "lf", "l", "да", "д", "нуы")
    no_answers = ("n", "no", "ytn", "н", "нет", "тщ", "т")
    params = ("name", "cabinet_name", "shelf_no", "folder_name", "doc_type", "serial", "product", "commentary")


class FileRecord:
    """
    Define the file in the archive.

    Params:
        name --- the file name;\n
        cabinet_name --- the name of the cabinet where the file is located;\n
        shelf_no --- the number of the shelf where the file is located;\n
        folder_name --- the name of the folder where the file is located;\n
        doc_type --- the document type;\n
        serial --- the serial_number;\n
        product --- the product;\n
        commentary --- the commentary to the file.\n
    """

    __slots__ = ("name", "cabinet_name", "shelf_no", "folder_name", "doc_type", "serial", "product", "commentary")

    attrs = ("name", "cabinet_name", "shelf_no", "folder_name", "doc_type", "serial", "product", "commentary")

    def __init__(self,
                 name: str,
                 cabinet_name: str = None,
                 shelf_no: int = None,
                 folder_name: str = None,
                 doc_type: str = None,
                 serial: str = None,
                 product: str = None,
                 commentary: str = None):
        self.name = name
        self.cabinet_name = cabinet_name
        self.shelf_no = shelf_no
        self.folder_name = folder_name
        self.doc_type = doc_type
        self.serial = serial
        self.product = product
        self.commentary = commentary

        Const.dict_file[self.name] = name

    def __str__(self):
        return f"File: name = {self.name}, cabinet name = {self.cabinet_name}, shelf number = {self.shelf_no}, " \
               f"folder name = {self.folder_name}, doc type = {self.doc_type}, serial = {self.serial}, " \
               f"product = {self.product}, commentary = \"{self.commentary}\""

    def __hash__(self):
        return hash((id(self), self.name))

    def __eq__(self, other):
        if isinstance(other, FileRecord):
            return self.name == other.name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, FileRecord):
            return self.name != other.name
        else:
            return NotImplemented

    def __getattribute__(self, key):
        if key in FileRecord.attrs:
            return object.__getattribute__(self, key)
        else:
            logging.warning(f"Attribute {key} is not appropriate and cannot be got.")
            return None

    def __setattr__(self, key, value):
        if key in FileRecord.attrs:
            object.__setattr__(self, key, value)
        else:
            logging.warning(f"Attribute {key} is not appropriate and cannot be set.")

    def check_values(self):
        if self.cabinet_name not in Const.list_cabinet_names:
            logging.warning(f"Cabinet name {self.cabinet_name} is not appropriate, change it.")
        if self.shelf_no not in Const.list_shelf_no:
            logging.warning(f"Shelf number {self.shelf_no} is not appropriate, change it.")
        if self.folder_name not in Const.list_folder_names:
            logging.warning(f"Folder name {self.folder_name} is not appropriate, change it.")
        if self.doc_type not in Const.list_doc_types:
            logging.warning(f"Doc type {self.doc_type} is not appropriate, change it.")

    def _convert_to_file(self):
        return self.name, self.cabinet_name, self.shelf_no, self.folder_name, self.doc_type, self.serial, \
               self.product, self.commentary


def user_approve():
    user_input = input("Do you want to apply the changes? Y/Д, N/Н\n").lower().strip()

    while True:
        if user_input in Const.yes_answers:
            return True
        elif user_input in Const.no_answers:
            return False
        else:
            print("Incorrect input.")


class JSONFile:
    """
    Define the JSON file.

    Params:
        path --- the path to the file;\n
        files --- the FileRecord instances;\n
        password --- the password;\n
        list_cabinet_names --- the list of allowed cabinet names;\n
        list_shelf_no --- the list of allowed shelf numbers;\n
        list_folder_names --- the list of allowed folder names;\n
        list_doc_types --- the list of allowed doc types;\n

    Properties:
        _is_validated --- the path verification;\n
        __content --- the JSON file content;\n
        parsed_file --- the dictionary of the JSON file;\n

    Functions:
        __password() --- get the password from the file;\n
        __list_cabinet_names() --- get the list of allowed cabinet names from the file;\n
        __list_shelf_no() --- get the list of allowed shelf numbers from the file;\n
        __list_folder_names() --- get the list of allowed folder names from the file;\n
        __list_doc_types() --- get the list of allowed doc types from the file;\n
        check_pass(user_input) --- verify the user-input password;\n
        get_files() --- get the FileRecord instances;\n
        __write_file() --- get the "file" values to write to the file;\n
        __write_params() --- get the "params" values to write to the file;\n
        write_to_json() --- write to the file;\n
    """

    def __init__(self, path: Union[str, Path]):
        self.path = path
        self.files = self.get_files()
        self.password = self.__password()
        self.list_cabinet_names = self.__list_cabinet_names()
        self.list_shelf_no = self.__list_shelf_no()
        self.list_folder_names = self.__list_folder_names()
        self.list_doc_types = self.__list_doc_types()

    def __str__(self):
        return f"JSON file: {Path(self.path).resolve()}, validated: {self._is_validated}"

    def __repr__(self):
        return f"JSONFile({self.path})"

    def __eq__(self, other):
        if isinstance(other, JSONFile):
            return self.path == other.path
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, JSONFile):
            return self.path != other.path
        else:
            return NotImplemented

    def __hash__(self):
        return hash((id(self), self.path))

    def __len__(self):
        return len(self.parsed_file)

    @property
    def _is_validated(self) -> bool:
        """
        Verify the JSON file.

        :return: the verification result.
        :rtype: bool
        """
        flag = False
        try:
            with open(self.path, "r") as file:
                json.load(file)
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError, {e.errno}, {e.strerror}.")
        except PermissionError as e:
            logging.error(f"PermissionError, {e.errno}, {e.strerror}.")
        except NameError as e:
            logging.error(f"NameError, {e.name}, {str(e)}.")
        except OSError as e:
            logging.error(f"OSError, {e.errno}, {e.strerror}.")
        except JSONDecodeError as e:
            logging.error(f"JSONDecodeError,{e.lineno}, {e.msg}.")
        else:
            flag = True
        finally:
            return flag

    @property
    def __content(self) -> Optional[dict]:
        """
        Get the JSON file content.

        :return: the Python dictionary.
        :rtype: dict or None
        """
        if self._is_validated:
            with open(self.path, "r") as file:
                content = json.load(file)
            return content
        else:
            logging.critical(f"File is incorrect.")
            exit()

    def __password(self) -> Optional[str]:
        """
        Get the password from the file.

        :return: the MD5 hashed password.
        :rtype: str or None
        """
        if self.__content["params"]["password"]:
            return None
        else:
            return self.__content["params"]["password"]

    def __list_cabinet_names(self) -> Optional[list[str]]:
        """
        Get the list of allowed cabinet names.

        :return: the list of cabinet names.
        :rtype: list[str] or None
        """
        return self.__content["params"]["list_cabinet_names"]

    def __list_shelf_no(self):
        return self.__content["params"]["list_shelf_no"]

    def __list_folder_names(self) -> Optional[list[str]]:
        """
        Get the list of allowed folder names.

        :return: the list of folder names.
        :rtype: list[str] or None
        """
        return self.__content["params"]["list_folder_names"]

    def __list_doc_types(self) -> Optional[list[str]]:
        """
        Get the list of allowed doc types.

        :return: the list of doc types.
        :rtype: list[str] or None
        """
        return self.__content["params"]["list_doc_types"]

    def check_pass(self, user_input: str) -> bool:
        """
        Check the user password.

        :param str user_input: the user password
        :return: the password verification.
        :rtype: bool
        """
        if self.password is None:
            return True
        else:
            # convert the user input to bytes
            user_pass = user_input.encode("utf-8")
            # get the MD5 hash
            md5_encoded = md5()
            md5_encoded.update(user_pass)
            # return the string representation
            user_input_encoded = md5_encoded.hexdigest()
            return user_input_encoded == self.__password

    def __getitem__(self, item):
        if item in Const.params:
            return [value[item] for value in self.__content["file"]]
        else:
            logging.info(f"KeyError, {item} is not an appropriate parameter.")
            return None

    @property
    def parsed_file(self) -> dict[str, list[dict[str, str]]]:
        """
        Get the file content as a Python dictionary.

        :return: the files.
        :rtype: dict[str, list[dict[str, str]]]
        """
        dict_content = dict()

        for item in self.__content["file"]:
            name = item["name"]
            dict_content[name] = []
            dict_content[name].append([item[param] for param in Const.params])
        return dict_content

    def get_files(self) -> list[FileRecord]:
        """
        Get the FileRecord instances.

        :return: the list of instances.
        :rtype: list[FileRecord]
        """
        files = []
        for key, value in self.parsed_file.items():
            files.append(FileRecord(
                key, self.__getitem__("cabinet_name"), self.__getitem__("shelf_no"), self.__getitem__("folder_name"),
                self.__getitem__("doc_type"), self.__getitem__("serial"), self.__getitem__("product"),
                self.__getitem__("commentary")))
        return files

    @staticmethod
    def __write_file() -> dict[str, list[dict[str, str]]]:
        """
        Set the "file" section.

        :return: the dictionary of the "file" section.
        :rtype: dict[str, list[dict[str, str]]]
        """
        dict_file = dict()
        dict_file["file"] = []
        for file in Const.dict_file.values():
            dict_file["file"].append(dict(zip(Const.params, file._convert_to_file())))
        return dict_file

    def __write_params(self) -> dict[str, dict[str, str]]:
        """
        Set the "params" section.

        :return: the dictionary of the "params" section.
        :rtype: dict[str, dict[str, str]]
        """
        dict_params = dict()
        dict_write = dict()
        # write the password
        if self.password is None:
            dict_write["password"] = ""
        else:
            dict_write["password"] = self.password
        # write the cabinet names
        dict_write["list_cabinet_names"] = self.list_cabinet_names
        # write the shelf numbers
        dict_write["list_shelf_no"] = self.list_shelf_no
        # write the folder names
        dict_write["list_folder_names"] = self.list_folder_names
        # write the doc types
        dict_write["list_doc_types"] = self.list_doc_types

        dict_params["params"] = dict_write
        return dict_params

    def write_to_json(self):
        """Write the current JSON file values to the file."""
        dict_to_json = {**self.__write_file(), **self.__write_params()}
        with open(self.path, "w") as file:
            file.write(json.dumps(dict_to_json, indent=2))


class _TempFile:

    attrs = ("name", "cabinet_name", "shelf_no", "folder_name", "doc_type", "serial", "product", "commentary")

    def __init__(self, file_name: str):
        self.file_name = file_name
        self._saved = False

        for attr in _TempFile.attrs:
            object.__setattr__(self, attr, getattr(self.file(), attr))

    def __str__(self):
        return f"Original: {self.file_name}, saved: {self._saved}"

    def __repr__(self):
        return f"_TempFile(file_name={self.file_name}, saved={self._saved})"

    def __hash__(self):
        return hash((id(self), self.file_name))

    def __key_eq(self):
        return self.file_name, self._saved

    def __eq__(self, other):
        if isinstance(other, _TempFile):
            return self.file_name == other.file_name
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _TempFile):
            return self.file_name == other.file_name
        else:
            return NotImplemented

    def file(self):
        return Const.dict_file[self.file_name]

    def write_file(self):
        for attr in _TempFile.attrs:
            object.__setattr__(self.file(), attr, getattr(self, attr))
        return self.file()


class User:
    def __init__(self, json_file: JSONFile, password: str):
        self.time = datetime.datetime.now()
        self.json_file = json_file
        self.password = password

    def __hash__(self):
        return hash((self.name, self.json_file, self.password))

    def __key(self):
        return self.name, self.time, self.password

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


    @property
    def _is_ok(self) -> bool:
        if self.json_file.check_pass(self.password):
            logging.info(f"User {self.name}, password {self.password} logged in.")
            return True
        else:
            logging.critical(f"User {self.name}, password {self.password} failed to log in.")
            return False


class _User:

    def __init__(self, user: User):
        if user._is_ok:
            self.user = user
            self.temp_files = []

    def __str__(self):
        return str(self.user)

    def __repr__(self):
        return repr(self.user)

    @property
    def name(self):
        return self.user.name

    @property
    def json_file(self) -> JSONFile:
        return self.user.json_file

    def read_file(self):
        return self.json_file.parsed_file

    @property
    def init_objects(self):
        return self.json_file.get_files()

    def init_object_names(self):
        return [file.name for file in self.init_objects]

    def find_file(self, attr: str, value):
        if attr in FileRecord.attrs:
            result = [file for file in self.init_objects if getattr(file, attr) == value]
            if not result:
                message = f"Found results:\n{result}"
                pprint(message)
                return result
            else:
                print("No files found.")
                return None
        else:
            logging.warning(f"Attribute {attr} is not appropriate.")
            print("Not appropriate request.")
            return None

    def find_file_name(self, value: str):
        return self.find_file("name", value)

    def modify_file(self, file: FileRecord, attr: str, value):
        temp_file = _TempFile(file.name)
        self.temp_files.append(temp_file)
        try:
            setattr(temp_file, attr, value)
        except AttributeError as e:
            logging.warning(f"AttributeError, {str(e)}.")
        except ValueError as e:
            logging.warning(f"ValueError, {str(e)}.")
        except NameError as e:
            logging.warning(f"NameError, {str(e)}.")
        finally:
            return temp_file

    def save_file(self, temp_file: _TempFile, approve: bool):
        if temp_file not in self.temp_files:
            logging.error(f"Internal error, saving {temp_file} that does not exist.")
        else:
            if temp_file._saved:
                logging.warning(f"The file {temp_file} has already been saved.")
                print("The file has already been saved.")
                self.temp_files.remove(temp_file)
            else:
                if approve:
                    temp_file.write_file()
                    temp_file._saved = True
                    self.temp_files.remove(temp_file)
                else:
                    self.temp_files.remove(temp_file)

    def create_file(
            self, name: str, /,
            cabinet_name: str = None,
            shelf_no: int = None,
            folder_name: str = None,
            doc_type: str = None,
            serial: str = None,
            product: str = None,
            commentary: str = None):
        # attrs = ("name", "cabinet_name", "shelf_no", "folder_name", "doc_type", "serial", "product", "commentary")
        if name in self.init_object_names():
            logging.warning(f"The name {name} already exists.")
            return None
        else:
            file = FileRecord(name, cabinet_name, shelf_no, folder_name, doc_type, serial, product, commentary)
            return file

    def delete_file(self, file_name: str):
        if file_name in self.init_object_names():
            file = self.find_file_name(file_name)

