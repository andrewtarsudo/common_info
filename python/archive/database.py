import sqlite3
from copy import copy
from sqlite3 import Connection, Cursor
from pathlib import Path
from typing import Union, Optional
from pprint import pprint
from archive_base import init_doc_classifications
from archive_base import DocType, DocShort, DocCategory, DocStandard, DocClassification, Const


def add_values():
    # type short category standard
    init_doc_classifications()
    return [(value.doc_type, value.doc_short, value.doc_category, value.doc_standard)
            for value in Const.dict_classification.values()]




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
    def connection(self) -> Connection:
        return sqlite3.Connection(self.path)

    def cursor(self) -> Cursor:
        return self.connection.cursor()

    @property
    def tables(self):
        return [item[0] for item in self.execute(query_get_tables())]

    def execute(self, query: str):
        try:
            res = [row for row in self.cursor().execute(query)]
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
            self.cursor().close()

    def commit_changes(self):
        self.connection.commit()

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
    path = '/Users/user/Desktop/archive.db'
    sql_db = SQLDatabase(path)
    print(add_values())
    for index, (doc_type, short, category, standard) in enumerate(add_values()):
        print(index)
        print(doc_type)
        print(short)
        print(category)
        print(standard)
        sql_db.cursor().execute("INSERT INTO classification values(?, ?, ?, ?, ?)", (index, doc_type, str(short), str(category), ""))
        sql_db.connection.commit()
    # pprint(sql_db.doc_class_category())
    sql_db.connection.commit()
    # pprint(sql_db.execute(query_select_all("sqlite_sequence")))


if __name__ == "__main__":
    main()
