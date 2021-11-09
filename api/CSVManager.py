from exception.DatabaseNotFoundException import DatabaseNotFoundException


class CSVManager:
    def __init__(self, database: str):
        self.database = database
        self.data = self.open()

    def open(self):
        try:
            file = open(self.database, "rw", encoding="utf-8")
            data = file.readlines()
            file.close()
        except FileNotFoundError:
            raise DatabaseNotFoundException
        return data

    def find(self, request: str):
        answer = []
        for line in self.data:
            if line.find(request) != -1:
                answer.append(line)
        return answer

    def save(self, dump: list):
        try:
            file = open(self.database, "w", encoding="utf-8")
            file.writelines(dump)
            file.close()
        except FileNotFoundError:
            raise DatabaseNotFoundException
