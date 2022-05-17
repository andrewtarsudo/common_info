import hashlib
from typing import Union, Optional
from pathlib import Path
import sqlite3


def query_select_all(table: str):
    return f"""SELECT * FROM {table}"""


def query_get_tables():
    return """SELECT name from sqlite_master WHERE type='table';"""


def query_select_record(table: str, attr: str, value: str):
    return f"""SELECT * FROM {table} WHERE {attr} = {value};"""


def query_select_column(table: str, column: str):
    return f"""SELECT {column} FROM {table};"""


def query_update_record(table: str, set_attr: str, set_value: str, attr: str, value: str):
    return f"""UPDATE {table} SET {set_attr} = {set_value} WHERE {attr} = {value};"""


def query_delete_record(table: str, attr: str, value: str):
    return f"""DELETE FROM {table} WHERE {attr} = {value};"""


def query_select_product_name(product_name: str):
    return query_select_record("product", "name", product_name)


def check_product_name(product_name: str):
    return product_name in query_select_column("product", "name")


def query_get_product_id(product_name: str):
    return query_select_record("product", "name", product_name)


class SQLDatabase:
    classifiers = ('doc_class_short', 'doc_class_category', 'doc_class_standard', 'doc_class_type')

    def __init__(self, path: Union[str, Path]):
        self.path = path

    @property
    def tables(self):
        return [item[0] for item in self.execute(query_get_tables())]

    def execute(self, query: str):
        connection = sqlite3.Connection()
        try:
            connection = sqlite3.Connection(self.path)
            cursor = connection.cursor()
            res = [row for row in cursor.execute(query)]
        except sqlite3.OperationalError as e:
            print(f"{e.sqlite_errorcode}, {e.sqlite_errorname}, {e.args}")
        except sqlite3.Error as e:
            print(f"SQL Connection Error {e.sqlite_errorcode}, {e.sqlite_errorname}. {e.args}")
            return None
        except AttributeError as e:
            print(f"{e.name}, {e.obj}, {e.args}")
        else:
            return res
        finally:
            connection.close()

    def _commit_changes(self, connection: sqlite3.Connection):
        connection.commit()
        connection.close()

    def __check_table_exists(self, table: str):
        return table in self.tables

    def doc_class_category(self) -> Optional[list[str]]:
        if self.__check_table_exists("doc_class_category"):
            query = query_select_all("doc_class_category")
            return [category for category, _ in self.execute(query)]
        else:
            print("No such table.")
            return None

    def doc_class_standard(self) -> Optional[list[str]]:
        if self.__check_table_exists("doc_class_standard"):
            query = query_select_all("doc_class_standard")
            return [standard for standard, _ in self.execute(query)]
        else:
            print("No such table.")
            return None

    def doc_class_type(self) -> Optional[list[str]]:
        if self.__check_table_exists("doc_class_type"):
            query = query_select_all("doc_class_type")
            return [doc_type for doc_type, _ in self.execute(query)]
        else:
            print("No such table.")
            return None

    def doc_class_short(self) -> Optional[list[str]]:
        if self.__check_table_exists("doc_class_short"):
            query = query_select_all("doc_class_short")
            return [short for short, _ in self.execute(query)]
        else:
            print("No such table.")
            return None

    def doc_classification(self):
        if self.__check_table_exists("classification"):
            query = query_select_all("classification")
            return self.execute(query)
        else:
            print("No such table.")
            return None

    def all_products(self):
        if self.__check_table_exists("product"):
            query = query_select_all("product")
            return self.execute(query)
        else:
            print("No such table.")
            return None

    def all_product_names(self):
        if self.__check_table_exists("product"):
            query = query_select_column("product", "name")
            return self.execute(query)
        else:
            print("No such table.")
            return None




def get_sha256(input_string: str) -> str:
    """
    Gets the SHA-256 hash of the file.

    :param str input_string: the line to encipher
    :return: the SHA-256 checksum in the hex format.
    :rtype: str
    """
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(input_string.encode("utf-8"))

    return hash_sha256.hexdigest()


def main():
    attempt = input("Введите строку для получения SHA-256 хэша:\n")
    print(f"SHA-256: {get_sha256(attempt)}")
    input("Нажмите любую клавишу, чтобы завершить работу ...")


if __name__ == '__main__':
    main()

