import sqlite3 as sq
import pandas as pd

conn = None
c = None
active_db = None


class FileTypeError(Exception):
    def __init__(self, types: list[str]) -> None:
        self.message = "Invalid file type. Accepted file types are: " + \
            ",".join(types)
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"FileTypeError: {self.message}"


def change_active_db(db_path: str) -> None:
    global active_db
    active_db = db_path


def connect_to_db(func):
    def wrap(*args, **kwargs):
        global conn, c
        change_active_db(args[-1])
        conn = sq.connect(active_db)
        c = conn.cursor()
        result = func(*args, **kwargs)
        conn.close()

        return result
    return wrap


@connect_to_db
def create_table(table_name: str, columns: list[str] | dict[str, str], db_path: str = "data/capitals.db") -> bool:
    try:
        if isinstance(columns, dict):
            to_list = [f"{k} {v}" for k, v in columns.items()]
            c.execute(f"CREATE TABLE IF NOT EXISTS {
                      table_name} ({", ".join(to_list)})")
        elif isinstance(columns, list):
            c.execute(f"CREATE TABLE IF NOT EXISTS {
                      table_name} ({", ".join(columns)})")
        else:
            raise TypeError("Columns must be of type 'dict' or 'list'")
        return True
    except TypeError as e:
        print(e)
        return False


# GET functions
@connect_to_db
def fetch_one(table_name: str, criteria: str, db_path: str = "data/capitals.db") -> tuple | None:
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name} WHERE {criteria}")
        row = c.fetchone()
        return row
    except sq.OperationalError as e:
        print(e)


@connect_to_db
def fetch_many(table_name: str, criteria: str, num_rows: int, db_path: str = "data/capitals.db") -> list[tuple] | None:
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name} WHERE {criteria}")
        rows = c.fetchmany(num_rows)
        return rows
    except sq.OperationalError as e:
        print(e)


@connect_to_db
def fetch_all(table_name: str, db_path: str = "data/capitals.db") -> list[tuple] | None:
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        return rows
    except sq.OperationalError as e:
        print(e)


# INSERT functions
@connect_to_db
def insert_row(table_name: str, row_data: tuple, db_path: str = "data/capitals.db") -> bool:
    try:
        table_name = table_name.lower()
        c.execute(f"INSERT INTO {table_name} VALUES {row_data}")
        conn.commit()
        return True
    except sq.OperationalError as e:
        print(e)
        return False
    except sq.IntegrityError as e:
        print(e)
        return False


@connect_to_db
def insert_rows(table_name: str, num_columns: int, rows_data: list[tuple], db_path: str = "data/capitals.db") -> bool:
    try:
        table_name = table_name.lower()
        qmarks = ['?' for _ in range(num_columns)]
        c.executemany(f"INSERT INTO {table_name} VALUES ({
                      ", ".join(qmarks)})", rows_data)
        conn.commit()
        return True
    except sq.OperationalError as e:
        print(e)
        return False
    except sq.IntegrityError as e:
        print(e)
        return False


# UPDATE functions
@connect_to_db
def update_row(table_name: str, criteria: str, updates: dict[str, str | int | float], db_path: str = "data/capitals.db") -> bool:
    try:
        table_name = table_name.lower()
        updates_list = []
        for col, val in updates.items():
            if type(val) == str:
                updates_list.append(f"{col} = '{val}'")
            else:
                updates_list.append(f"{col} = {val}")
        c.execute(f"UPDATE {table_name} SET {
                  ", ".join(updates_list)} WHERE {criteria}")
        conn.commit()
        return True
    except sq.OperationalError as e:
        print(e)
        return False


# DELETE function
@connect_to_db
def delete_row(table_name: str, criteria: dict[str, str], db_path: str = "data/capitals.db") -> bool:
    try:
        table_name = table_name.lower()
        if "and" not in criteria.keys() and "or" not in criteria.keys():
            criteria_str = criteria["primary"]
        elif "and" in criteria.keys() and len(criteria["and"]) >= 1:
            criteria_str = f"{criteria["primary"]}{
                " AND ".join(criteria["and"])}"
        elif "or" in criteria.keys() and len(criteria["or"]) >= 1:
            criteria_str = f"{criteria["primary"]}{
                " OR ".join(criteria["and"])}"

        c.execute(f"DELETE FROM {table_name} WHERE {criteria_str}")
        conn.commit()
        return True
    except sq.OperationalError as e:
        print(e)
        return False


# LOAD functions
def datetime_to_string(serial_date: pd.Timestamp, db_path: str = "data/capitals.db") -> str:
    year = serial_date.year
    month = serial_date.month_name()
    day = serial_date.day
    return f"{month[:3]} {day}, {year}"


@connect_to_db
def load_file(filepath: str, filename: str, table_name: str, drop_columns: list[str], write_type: str = "replace", db_path: str = "data/capitals.db") -> None:
    # format full filename
    if filepath[-1] in ("/", "\\"):
        file_to_load = f"{filepath}{filename}"
    else:
        file_to_load = f"{filepath}/{filename}"

    # read the file
    try:
        if filename.endswith(".xlsx"):
            df = pd.read_excel(file_to_load)
        elif filename.endswith(".csv"):
            df = pd.read_csv(file_to_load)
        else:
            raise FileTypeError([".xlsx", ".csv"])
    except FileTypeError as e:
        print(e)
        return
    except Exception as e:
        print(e)
        return

    # drop columns
    if len(drop_columns) >= 1:
        df.drop(columns=drop_columns, inplace=True)

    # Convert date stamps to strings
    if "Born" in df.columns:
        bdays = []
        for bday in df["Born"]:
            bdays.append(datetime_to_string(bday))
        df["Born"] = pd.Series(bdays)

    # Convert punctuation in height column (' -> ft, " -> in)
    if "Ht" in df.columns:
        hts = []
        for ht in df["Ht"]:
            new_ht = ht.replace("'", "ft ").replace("\"", "in")
            hts.append(new_ht)
        df["Ht"] = pd.Series(hts)

    # write to db
    if write_type not in ("fail", "replace", "append"):
        write_type = "replace"
    df.to_sql(table_name, conn, if_exists=write_type, index=False)


if __name__ == '__main__':
    ...
