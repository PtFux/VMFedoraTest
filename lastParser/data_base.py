#!/usr/bin/env python
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
    user: str = 'postgres'
    password: str = 'postgres'
    host: str = 'localhost'

    def get_params(self):
        return {
                # "dbname": self.dbname,
                "user": self.user,
                "password": self.password,
                "host": self.host,
                "port": "5432"}


class PostgresDB:
    def __init__(self, params: ParamData = ParamData()):
        self._count_insert = 0
        self.params = params
        self.connection = None

    def init_db(self):
        self.connection = psycopg2.connect(user="polina",
                                           database="my_parser",
                                           password="password",
                                           host="127.0.0.1",
                                           port="5432")
        # cursor = self.conn.cursor()

    def create_table(self):
        pass

    def check_db(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            res = cursor.fetchone()
        return res

    def insert_one(self, prod: dict):
        _id = str(hash(prod.get("name")))
        prod.update({"_id": _id})
        self._count_insert += 1

        print(f"[{self._count_insert}] {prod}")

    def select(self):
        pass


if __name__ == "__main__":
    pos = PostgresDB()
    pos.init_db()
    print(pos.check_db())
