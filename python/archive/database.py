import os
import sqlite3
import sys
from pathlib import Path
from typing import Union, Optional
from pprint import pprint
import datetime
import logging
import hashlib


def query_get_tables():
    return """SELECT name from sqlite_master WHERE type='table';"""


def query_select_all(table: str):
    return f"""SELECT * FROM {table}"""


def query_select_record(table: str, attr: str, value: str):
    return f"""SELECT * FROM {table} WHERE {attr} = {value};"""


def get_sha256(input_string: str) -> str:
    """
    Gets the SHA-256 hash of the file.

    :param str input_string: the line to encrypt
    :return: the SHA-256 checksum in the hex format.
    :rtype: str
    """
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(input_string.encode("utf-8"))

    return hash_sha256.hexdigest()


class User:
    def __init__(self, db_path: Union[Path, str], password: str):
        self.time = datetime.datetime.now()
        self.db_path = Path(db_path).resolve()
        self.password = password

    def __hash__(self):
        return hash((self.name, self.password))

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
        if self._user_system.sysname == "Windows":
            key = "USERNAME"
        else:
            key = "USER"
        return os.environ[key]

    @property
    def _user_system(self):
        return os.uname()

    def __trusted_names(self):
        connection = sqlite3.Connection()
        try:
            connection = sqlite3.Connection(self.db_path.with_name("trusted.db"))
            cursor = connection.cursor()
            result = [item for item in cursor.execute("SELECT name FROM trusted")]
        except sqlite3.ProgrammingError as e:
            logging.error(
                f"ProgrammingError: {str(e)}. User: {self.name}, OS: {self._user_system}, datetime: {self.time}")
            return None
        except sqlite3.DatabaseError as e:
            logging.error(
                f"DatabaseError: {str(e)}. User: {self.name}, OS: {self._user_system}, datetime: {self.time}")
            return None
        except sqlite3.Error as e:
            logging.error(
                f"Error: {str(e)}. User: {self.name}, OS: {self._user_system}, datetime: {self.time}")
            return None
        else:
            return result
        finally:
            connection.close()

    def _all_allowed(self):
        return "all" in self.__trusted_names()

    def _trusted(self):
        if self.__trusted_names():
            sys.exit("Sorry, some problems with the database. Please, connect back later.")
        else:
            if self.name not in self.__trusted_names():
                logging.warning(
                    f"AUTHORIZATION: NOT TRUSTED. User: {self.name}, OS: {self._user_system}, datetime: {self.time}")
                sys.exit("Sorry, you are not a trusted user. You are not welcome. Get out of here.")

    def __hashed_password(self):
        connection = sqlite3.Connection()
        try:
            connection = sqlite3.Connection(self.db_path.with_name("trusted.db"))
            cursor = connection.cursor()
            result = cursor.execute("SELECT password FROM trusted WHERE name = ?", (self.name,))
        except sqlite3.ProgrammingError as e:
            logging.error(
                f"ProgrammingError: {str(e)}. User: {self.name}, OS: {self._user_system}, datetime: {self.time}")
            return None
        except sqlite3.DatabaseError as e:
            logging.error(
                f"DatabaseError: {str(e)}. User: {self.name}, OS: {self._user_system}, datetime: {self.time}")
            return None
        except sqlite3.Error as e:
            logging.error(
                f"Error: {str(e)}. User: {self.name}, OS: {self._user_system}, datetime: {self.time}")
            return None
        else:
            return result.fetchone()
        finally:
            connection.close()

    @property
    def verify_password(self) -> bool:
        if self._all_allowed():
            logging.info(
                f"AUTHORIZATION: SUCCESS ALL. User {self.name}, OS: {self._user_system}, datetime: {self.time}.")
            return True
        hashed_password = get_sha256(self.password)
        if hashed_password == self.__hashed_password():
            logging.info(
                f"AUTHORIZATION: SUCCESS. User {self.name}, password {self.password}, "
                f"OS: {self._user_system}, datetime: {self.time}.")
            return True
        else:
            logging.info(f"AUTHORIZATION: FAIL. User {self.name}, password {self.password}, OS: {self._user_system}.")
            return False


class _User:
    def __init__(self, user: User):
        if user.verify_password:
            self.user = user

    def __str__(self):
        return str(self.user)

    def __repr__(self):
        return repr(self.user)

    @property
    def name(self):
        return self.user.name

    @property
    def db_path(self):
        return self.user.db_path

    def get_tables(self) -> Optional[list[str]]:
        connection = sqlite3.Connection(self.db_path)
        cursor = connection.cursor()
        tables = [row for row in cursor.execute(query_get_tables())]
        connection.close()
        return tables

    def __products(self):
        connection = sqlite3.Connection(self.db_path)
        cursor = connection.cursor()
        products = [row for row in cursor.execute(query_select_all("product"))]
        attrs = cursor.description
        connection.close()
        return products, attrs

    def get_products(self):
        products, _ = self.__products()
        return products

    def get_product_attrs(self):
        _, attrs = self.__products()
        return attrs

    def start_end(self, func):
        def wrapper(*args, **kwargs):
            connection = sqlite3.Connection(self.db_path)
            cursor = connection.cursor()
            func()
            connection.close()
            return func()
        return wrapper()

    @start_end
    def search_product(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor, product_name: str):
        cursor_product = cursor.execute(query_select_record("product", "name", product_name))
        return cursor_product.fetchone()

    def get_product_docs(self, product_name: str):
        pass


def create_database():
    sqlite_connection = sqlite3.Connection("database.db")
    cursor = sqlite_connection.cursor()
    sqlite_version = "SELECT sqlite_version();"
    cursor.execute(sqlite_version)
    record = cursor.fetchall()
    print(record)
    cursor.close()
    sqlite_connection.close()


def create_table():
    sqlite_connection = sqlite3.Connection("database.db")
    sqlite_create_table = """CREATE TABLE test (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE);"""
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()


def main():
    filename = "./basic_log.log"
    fmt = "%(levelName)s %(asctime)s, %(funcName) --- %(message)s"
    level = logging.INFO
    logging.basicConfig(filename=filename, format=fmt, level=level)

    path = '/Users/user/Desktop/archive.db'

    connection = sqlite3.Connection(path)
    cursor = connection.cursor()


if __name__ == "__main__":
    main()
