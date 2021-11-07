import sqlite3

from exception.DatabaseNotFoundException import DatabaseNotFoundException
from exception.InvalidSQLRequestException import InvalidSQLRequestException


class SQLTableManager:
    def __init__(self, database):
        self.database = database

    def connect_to_database(self):
        try:
            self.connection = sqlite3.connect(self.database)
            self.cursor = self.connection.cursor()
        except Exception:
            raise DatabaseNotFoundException

    def close_database(self):
        self.connection.close()

    def execute_request(self, request):
        try:
            return self.cursor.execute(request).fetchall()
        except Exception:
            return InvalidSQLRequestException

    def get_table_list(self):
        answer = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        return [table[0] for table in answer]

    def get_columns(self, table):
        answer = self.connection.execute(f"SELECT * FROM {table}")
        return [description[0] for description in answer.description]
