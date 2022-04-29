import datetime
import pathlib
import os
from copy import copy
from typing import Optional
import logging

basic_logger = logging.basicConfig("")


class Const:
    dict_ward_id = dict()
    dict_shelf_id = dict()
    dict_file_id = dict()

    list_doc_types = []

    yes_answers = ("y", "yes", "lf", "l", "да", "д", "нуы")
    no_answers = ("n", "no", "ytn", "н", "нет", "тщ", "т")
    
    allowed = ["bochkova", "tarasov-a", "AndrewTarasov"]


class Ward:
    index = 0

    __slots__ = ("identifier", "ward_name", "shelf_id")

    def __init__(self,
                 ward_name: str = None,
                 shelf_id: list[int] = None):
        if shelf_id is None:
            shelf_id = []
        self.identifier = Ward.index
        if ward_name is None:
            ward_name = str(self.identifier)
        self.ward_name = ward_name
        self.shelf_id = shelf_id

        Const.dict_ward_id[self.identifier] = self
        Ward.index += 1

    def __shelves(self):
        return [Const.dict_shelf_id[shelf] for shelf in self.shelf_id]

    def __files(self):
        return [Const.dict_file_id[file] for shelf in self.__shelves() for file in shelf]

    def __hash__(self):
        return hash((self.identifier, self.name))

    def __key(self):
        return self.identifier, self.name

    def __eq__(self, other):
        if isinstance(other, Ward):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Ward):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __contains__(self, item):
        if isinstance(item, Shelf):
            return item in self.__shelves()
        elif isinstance(item, FileRecord):
            return item in self.__files()
        else:
            return NotImplemented

    def __iter__(self):
        return (shelf for shelf in self.__shelves())

    def __getitem__(self, key):
        if not isinstance(key, int):
            print(f"__getitem__, AttributeError, {key} must be integer.")
            return None
        else:
            if key not in Const.dict_shelf_id:
                print(f"KeyError, {key} is not an appropriate item.")
                return None
            else:
                return Const.dict_shelf_id[key]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            Const.dict_shelf_id[key] = value
        else:
            print(f"__setitem__, KeyError, {key} is not an appropriate item.")
            logging.info("Ward.__setitem__", key, self.identifier,)

    def __len__(self):
        return len(self.__files())

    def __getattribute__(self, attr):
        if attr in ("identifier", "name", "shelf_id"):
            return object.__getattribute__(self, attr)
        elif attr in ("shelf_number", "file_id"):
            return [shelf.__getattribute__(attr) for shelf in self.__shelves()]
        elif attr in ("idx", "name", "doc_type", "serial_number", "product_type"):
            return [file.__getattribute__(attr) for file in self.__files()]
        else:
            print(f"__getattribute__, AttributeError, {attr} is not an appropriate attribute.")
            return None


class Shelf:
    index = 0

    def __init__(self,
                 ward_id: int,
                 shelf_number: int,
                 file_id: list[int] = None):
        if file_id is None:
            file_id = []
        self.identifier = Shelf.index
        self.ward_id = ward_id
        self.shelf_number = shelf_number
        self.file_id = file_id

        Const.dict_shelf_id[self.identifier] = self
        Shelf.index += 1

    __slots__ = ("ward_id", "shelf_number", "file_id", "identifier")

    def __ward(self):
        return Const.dict_ward_id[self.ward_id]

    def __files(self):
        return [Const.dict_file_id[file] for file in self.file_id]

    def __hash__(self):
        return hash((self.identifier, self.ward_id, self.shelf_number))

    def __key(self):
        return self.identifier, self.ward_id, self.shelf_number

    def __eq__(self, other):
        if isinstance(other, Shelf):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Shelf):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def __contains__(self, item):
        if isinstance(item, FileRecord):
            return item in self.__files()
        else:
            return NotImplemented

    def __iter__(self):
        return (file for file in self.__files())


class FileRecord:
    index = 0

    __slots__ = ("name", "ward_id", "shelf_id", "doc_type", "serial_number", "product_type", "identifier")

    def __init__(self,
                 name: str,
                 ward_id: int,
                 shelf_id: int,
                 doc_type: str = None,
                 serial_number: str = None,
                 product_type: str = None):
        self.name = name
        self.ward_id = ward_id
        self.shelf_id = shelf_id
        self.doc_type = doc_type
        self.product_type = product_type
        self.serial_number = serial_number
        self.identifier = FileRecord.index

        Const.dict_file_id[self.identifier] = self
        FileRecord.index += 1

    def __hash__(self):
        return hash((self.identifier, self.name))

    def __key(self):
        return self.identifier, self.name

    def __eq__(self, other):
        if isinstance(other, FileRecord):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, FileRecord):
            return self.__key() != other.__key()
        else:
            return NotImplemented


class _RawFile:
    __slots__ = ("file_id", "_approved", "identifier")

    def __init__(self, file_id: int):
        self.file_id = file_id
        self._approved = False
        self.identifier = self.id

    def __str__(self):
        if self._approved:
            string_approve: str = "approved"
        else:
            string_approve: str = "not approved"
        return f"File {Const.dict_file_id[self.file_id]} is in ward {self.__ward}, on shelf {self.__shelf}, " \
               f"{string_approve}"

    def __repr__(self):
        return f"_RawFile(file_id={self.file_id}, _approved={self._approved})"

    def __key(self):
        return self.id, self.file_id

    def __hash__(self):
        return hash((self.identifier, self.name))

    def __eq__(self, other):
        if isinstance(other, _RawFile):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, _RawFile):
            return self.__key() != other.__key()
        else:
            return NotImplemented

    def approve(self, user_input: Optional[bool]):
        if user_input is None:
            print("Incorrect input.")
            return None
        else:
            self._approved = user_input

    def __file(self) -> FileRecord:
        return copy(Const.dict_file_id[self.file_id])

    def __ward_id(self) -> int:
        return self.__file().ward_id

    def __ward(self) -> Ward:
        return Const.dict_ward_id[self.__ward_id()]

    def __shelf(self):
        return Const.dict_shelf_id[self.shelf_id]

    def __file_original(self) -> FileRecord:
        return Const.dict_file_id[self.file_id]

    def __getattribute__(self, attr):
        if attr in ("ward_id", "shelf_id", "name", "identifier", "file_id", "_approved"):
            return object.__getattribute__(self, attr)
        elif attr in ("idx", "name", "doc_type", "serial_number", "product_type", "identifier"):
            return object.__getattribute__(self.__file(), attr)
        else:
            print(f"__getattribute__, AttributeError, {attr} is not an appropriate attribute.")
            return None

    def update(self):
        if self._approved:
            for attr in ("idx", "name", "doc_type", "serial_number", "product_type", "identifier"):
                setattr(self.__file_original(), attr, getattr(self, attr))
                print("The file is modified.")
        else:
            print("The changes are not approved.")


def user_approve():
    user_input = input("Do you want to apply the changes? Y/Д, N/Н\n").lower().strip()

    while True:
        if user_input in Const.yes_answers:
            return True
        elif user_input in Const.no_answers:
            return False
        else:
            print("Incorrect input.")


class User:
    def __init__(self):
        self.time = datetime.datetime.now()

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
