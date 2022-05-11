import sqlite3
from sqlite3 import Connection, Cursor
from enum import Enum
from pathlib import Path
from typing import Union, Optional


def query_select_all(table: str):
    return f"""SELECT * FROM {table}"""


def query_select_record(table: str, attr: str, value: str):
    return f"""SELECT * FROM {table} WHERE {attr} = {value}"""


def query_select_column(table: str, column: str):
    return f"""SELECT {column} FROM {table}"""


def query_update_record(table: str, set_attr: str, set_value: str, attr: str, value: str):
    return f"""UPDATE {table} SET {set_attr} = {set_value} WHERE {attr} = {value}"""


def query_delete_record(table: str, attr: str, value: str):
    return f"""DELETE FROM {table} WHERE {attr} = {value}"""


def query_select_product_name(product_name: str):
    return query_select_record("product", "name", product_name)


def check_product_name(product_name: str):
    return product_name in query_select_column("product", "name")


def query_get_product_id(product_name: str):
    return query_select_record("product", "name", product_name)


class SQLDatabase:
    def __init__(self, path: Union[str, Path]):
        self.path = path

    def __execute(self, queries: list[str]):
        try:
            with Connection(self.path).cursor() as cursor:
                for query in queries:
                    cursor.execute(query)
        except sqlite3.Error as e:
            print(f"SQL Connection Error {e.sqlite_errorcode}, {e.sqlite_errorname}. {e.args}")
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
    create_table()


if __name__ == "__main__":
    main()
