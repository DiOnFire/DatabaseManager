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
