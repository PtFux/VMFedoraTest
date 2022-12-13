from dataclasses import dataclass

import psycopg2


class MongoDB:
    def __init__(self):
        self._count_insert = 0

    def init_db(self):
        pass

    def create_collection(self):
        pass

    def insert_one(self, prod: dict):
        _id = str(hash(prod.get("name")))
        prod.update({"_id": _id})
        self._count_insert += 1

        print(f"[{self._count_insert}] {prod}")

    def find(self):
        pass


@dataclass
class ParamData:
    dbname: str = 'my_parser'
    user: str = 'polina'
    password: str = 'password'
    host: str = 'localhost'

    def dict(self):
        return {"dbname": self.dbname,
                "user": self.user,
                "password": self.password,
                "host": self.host}


class PostgresDB:
    def __init__(self, params: ParamData = ParamData()):
        self._count_insert = 0

        self.params = params
        self.conn = None
        self.cursor = None

    def init_db(self):
        self.conn = psycopg2.connect(**self.params.dict())
        self.cursor = self.conn.cursor()

    def create_table(self):
        pass

    def insert_one(self, prod: dict):
        _id = str(hash(prod.get("name")))
        prod.update({"_id": _id})
        self._count_insert += 1

        print(f"[{self._count_insert}] {prod}")

    def select(self):
        pass
