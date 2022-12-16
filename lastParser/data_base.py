#!/usr/bin/env python
from dataclasses import dataclass

import psycopg2


@dataclass
class ParamData:
    database: str = "my_parser"
    user: str = 'polina'
    password: str = 'password'
    host: str = 'localhost'
    port: str = "5432"

    def get_params(self):
        return {
                "user": self.user,
                "database": self.database,
                "password": self.password,
                "host": self.host,
                "port": self.port}


class PostgresDB:
    def __init__(self, params: ParamData = ParamData()):
        self._count_insert = 0
        self.params = params
        self.connection = None

    def init_db(self):
        self.connection = psycopg2.connect(**self.params.get_params())
        # cursor = self.conn.cursor()

    def create_table(self, name_table: str, category: dict):
        # create a new table
        with self.connection.cursor() as cursor:
            req = ""
            for cat in category.keys():
                req += '\n'
                req += f"{cat} {' '.join(category.get(cat))},"
            if req:
                req = req[:-1]

            print(f"CREATE TABLE {name_table}({req});")
            res = cursor.execute(f"CREATE TABLE {name_table}({req});")

        return res

    def check_db_version(self):
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

    def check_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema','pg_catalog');""")
            res = cursor.fetchall()
        return res

    def drop_table(self, name_table: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""DROP TABLE {name_table};""")

    def check_elem(self, elem, column: str, name_table: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM {name_table} WHERE {column} = {elem};""")
            res = cursor.fetchone()
        return res

    def insert(self, name_table: str, values: tuple):
        if self.check_elem(f"'{values[0]}'", column="_id", name_table=name_table):
            return

        req = f"INSERT INTO {name_table} VALUES {values};"
        # print(req)
        with self.connection.cursor() as cursor:
            cursor.execute(req)

    def select_everything(self, name_table: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM {name_table};""")
            res = cursor.fetchall()
        return res

    def close_connection(self):
        self.connection.commit()
        self.connection.close()

    def commit_connection(self):
        self.connection.commit()

    def my_select(self, req: str):
        with self.connection.cursor() as cursor:
            cursor.execute(req)
            res = cursor.fetchall()
        return res


if __name__ == "__main__":
    from random import randint

    print("Hello")
    pos = PostgresDB()
    pos.init_db()
    print(pos.check_db_version())

    # name = "test_table"
    # elems = {"id": ("INT", ),
    #          "name": ("TEXT",)}
    #
    # print(pos.create_table(name, elems))
    # print("TABLES", pos.check_tables())
    # print((name, ) in pos.check_tables())

    # print(*pos.select_everything("lavka"), sep='\n')
    # # pos.drop_table("lavka")
    #
    # ForPostgresColumns = {"_id": ("TEXT", "UNIQUE"),
    #                      "name": ("TEXT", ),
    #                      "price": ("INT", ),
    #                      "calories": ("FLOAT", ),
    #                      "proteins": ("FLOAT", ),
    #                      "fats": ("FLOAT", ),
    #                      "carbohydrates": ("FLOAT", )}


    # print(pos.check_elem("'8685717525016820902'", column="_id", name_table="lavka"))

    req = """
        SELECT floor(proteins * 100 / calories) as protein, *
        FROM lavka
        WHERE calories > 0 and proteins > 0
        ORDER BY protein DESC, price
        LIMIT 25
        """
    res = pos.my_select(req)
    print(*res, sep='\n')

    pos.close_connection()


