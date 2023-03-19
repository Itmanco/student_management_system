import sqlite3
import mysql.connector


class DbHelper:
    def __init__(self, database_path, dbtype, parameters = None):

        if dbtype == "sqlite":
            # Establish a connection and a cursor
            self.connection = sqlite3.connect(database_path)
            self.cursor = self.connection.cursor()
        else:
            self.host = parameters[0][1]
            self.user = parameters[1][1]
            self.password = parameters[2][1]
            self.database = parameters[3][1]

            # Establish a connection and a cursor
            self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                                      database=self.database)
            self.cursor = self.connection.cursor()

    def query_all(self, table_name):
        """
        select all data in the table
        :param table_name:
        :return:
        """
        # Query all data
        try:
            self.cursor.execute(f"select * from {table_name}")
            return self.cursor.fetchall()
        except sqlite3.OperationalError:
            return "no such table"

    def item_in_table(self, table_name, values):
        """
        :param table_name:
        :param values: array of tuples with conditions
                Format: [("column_name","number_value"),("column_name","'str_value'"),...]
        :return: rows than meet the conditions
        """
        first_cycle = True
        script = f"SELECT * FROM '{table_name}' WHERE "
        for item in values:
            if first_cycle:
                script = script + f"{item[0]}={item[1]}"
                first_cycle = False
            else:
                script = script + f" AND {item[0]}={item[1]}"

        self.cursor.execute(script)
        return self.cursor.fetchall()

    def create_table(self, table_name, columns):
        """
        :param table_name:
        :param columns: array of tuples with columns information
                Format: []
        :return: None
        """
        first_cycle = True
        script = f"CREATE TABLE '{table_name}' ("
        for item in columns:
            if first_cycle:
                if item[1] == "str":
                    script = script + f"'{item[0]}' TEXT"
                elif item[1] == "int":
                    script = script + f"'{item[0]}' INTEGER"
                first_cycle = False
            elif item[1] == "str":
                script = script + f",'{item[0]}' TEXT"
            elif item[1] == "int":
                script = script + f",'{item[0]}' INTEGER"
        script = script+")"
        self.cursor.execute(script)
        self.connection.commit()

    def query_with_condition(self, table_name, condition):
        # Query all data
        self.cursor.execute(f"select * from {table_name} WHERE {condition}")
        return self.cursor.fetchall()

    def insert_single(self, table_name, row):
        """
        #"cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",name_arg, course_arg, mobile_arg)"
        :param table_name:
        :param row:
        :return:
        """
        script = f"INSERT INTO {table_name} ("

        first_time = True
        for item in row:
            if first_time:
                first_time = False
                script = script + f"{item[0]}"
            else:
                script = script + f",{item[0]}"
        script = script+") VALUES ("

        first_time = True
        for item in row:
            if first_time:
                first_time = False
                script = script + f"'{item[1]}'"
            else:
                script = script + f",'{item[1]}'"
        script = script+")"
        self.cursor.execute(script)
        self.connection.commit()
        return 0

    def update_single(self, table_name, row, conditions):
        """

        :param table_name:
        :param row:
        :param conditions:
        :return:
        """
        first_time = True
        for item in row:
            if first_time:
                first_time = False
                script = f"UPDATE {table_name} SET {item[0]} = '{item[1]}'"
            else:
                script = script + f", {item[0]} = '{item[1]}'"

        first_time = True
        for item in conditions:
            if first_time:
                first_time = False
                script = script + f" WHERE {item[0]} = '{item[1]}'"
            else:
                script = script + f", {item[0]} = '{item[1]}'"

        self.cursor.execute(script)
        self.connection.commit()
        return 0

    def delete_rows(self, table_name, conditions):
        """
        DELETE from table_name WHERE condition[0] = 'condition[1]'
        :param table_name:
        :param conditions: list of tuples (item[0] = column name, item[1] = condition value
        :return:
        """
        first_time = True
        for item in conditions:
            if first_time:
                first_time = False
                script = f"DELETE from {table_name} where {item[0]} = '{item[1]}'"
            else:
                script = script + f", {item[0]} = '{item[1]}'"

        self.cursor.execute(script)
        self.connection.commit()
        return 0

    def insert_many_rows(self, table_name, rows):
        self.cursor.executemany(f"INSERT INTO {table_name} VALUES (?,?,?)", rows)
        self.connection.commit()
        return 0