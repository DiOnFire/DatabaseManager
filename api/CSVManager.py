from exception.DatabaseNotFoundException import DatabaseNotFoundException


class CSVManager:
    def __init__(self, database: str):
        self.database = database
        self.data = self.open()

    def open(self):
        try:
            file = open(self.database, "r", encoding="utf-8")
            data = file.readlines()
            for i in range(0, len(data) - 1):
                data[i] = data[i].strip("\n")
            file.close()
        except FileNotFoundError:
            file = open(self.database, "w", encoding="utf-8")
            data = []
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
            for line in dump:
                file.write(line + "\n")
            file.close()
        except FileNotFoundError:
            raise DatabaseNotFoundException

    def add_column(self, dump: list):
        self.save(self.data + dump)
