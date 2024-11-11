"""This module contains functions for interacting with databases"""

import sqlite3 as sq
import pandas as pd
import os

conn = None
c = None
active_db = None


class FileTypeError(Exception):
    """`FileTypeError` to be used when using a file other than `.xlsx` or `.csv`"""

    def __init__(self, types: list[str]) -> None:
        self.message = "Invalid file type. Accepted file types are: " + \
            ",".join(types)
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"FileTypeError: {self.message}"


def change_active_db(db_path: str) -> None:
    """Changes `global active_db` to be used by `sqlite3.connect()`"""
    global active_db
    active_db = db_path


def connect_to_db(func):
    """Wrapper function for any function that needs to access the database.\n
    Contains the `sqlite3` connection and cursor objects."""
    def wrap(*args, **kwargs):
        global conn, c

        # Change database before cursor
        if args[-1].endswith(".db"):
            change_active_db(args[-1])
        else:
            change_active_db("data/capitals.db")

        conn = sq.connect(active_db)
        c = conn.cursor()
        result = func(*args, **kwargs)
        conn.close()

        return result
    return wrap


@connect_to_db
def create_table(table_name: str, columns: list[str] | dict[str, str], db_path: str = "data/capitals.db") -> bool:
    """Creates a table in a database if it doesn't already exist.\n
    The `.db` file will be created if it doesn't exist.

    Args:
        table_name (str): name of the table to be created
        columns (list[str] | dict[str, str]): column names and dtypes (e.g. `["col1 text", ...]`, `{"col1": "text", ...}`)
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Raises:
        TypeError: occurs when `columns` is not of type `dict` or `list`

    Returns:
        bool: `True` if successful else `False`
    """
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
        print(f"ERROR: {e}")
        return False


# GET functions
@connect_to_db
def fetch_one(table_name: str, criteria: str, db_path: str = "data/capitals.db") -> tuple | None:
    """Fetches a single row from a database table

    Args:
        table_name (str): table to be queried
        criteria (str): SQL string for search criteria. may include logic operators (e.g. `col1 = 'yellow'`)
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        tuple|None: returns a tuple of the row data else if exists else `None`
    """
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name} WHERE {criteria}")
        row = c.fetchone()
        return row
    except sq.OperationalError as e:
        print(f"ERROR: {e}")


@connect_to_db
def fetch_many(table_name: str, criteria: str, num_rows: int, db_path: str = "data/capitals.db") -> list[tuple] | None:
    """Fetches multiple rows from a database table

    Args:
        table_name (str): table to be queried
        criteria (str): SQL string for search criteria. may include logic operators (e.g. `col1 = 'yellow'`)
        num_rows (int): maximum number of rows to be returned
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        list[tuple]|None: returns a list of row tuples if exist else `None`
    """
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name} WHERE {criteria}")
        rows = c.fetchmany(num_rows)
        return rows
    except sq.OperationalError as e:
        print(f"ERROR: {e}")


@connect_to_db
def fetch_all(table_name: str, db_path: str = "data/capitals.db") -> list[tuple] | None:
    """Fetches all rows from a database table

    Args:
        table_name (str): name of table to be queried
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        list[tuple]|None: returns a list of row tuples if table exists else `None`
    """
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        return rows
    except sq.OperationalError as e:
        print(f"ERROR: {e}")


# INSERT functions
@connect_to_db
def insert_row(table_name: str, row_data: tuple, db_path: str = "data/capitals.db") -> bool:
    """Adds a row to the end of a database table

    Args:
        table_name (str): table to insert row into
        row_data (tuple): tuple of the data to be inserted, separated by column
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        bool: `True` if successful else `False`
    """
    try:
        table_name = table_name.lower()
        c.execute(f"INSERT INTO {table_name} VALUES {row_data}")
        conn.commit()
        return True
    except sq.OperationalError as e:
        print(f"ERROR: {e}")
        return False
    except sq.IntegrityError as e:
        print(f"ERROR: {e}")
        return False


@connect_to_db
def insert_rows(table_name: str, rows_data: list[tuple], db_path: str = "data/capitals.db") -> bool:
    """Adds multiple rows to the end of a database table

    Args:
        table_name (str): table to insert rows into
        rows_data (list[tuple]): list of row tuples to be inserted. all tuples must be the same length as the number of columns in the table
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        bool: `True` if successful else `False`
    """
    try:
        table_name = table_name.lower()
        qmarks = len(rows_data[0])
        c.executemany(f"INSERT INTO {table_name} VALUES ({
                      ", ".join(qmarks)})", rows_data)
        conn.commit()
        return True
    except sq.OperationalError as e:
        print(f"ERROR: {e}")
        return False
    except sq.IntegrityError as e:
        print(f"ERROR: {e}")
        return False


# UPDATE functions
@connect_to_db
def update_row(table_name: str, criteria: str, updates: dict[str, str | int | float], db_path: str = "data/capitals.db") -> bool:
    """Updates a row in a database table

    Args:
        table_name (str): table to be updated
        criteria (str): SQL string for search criteria. may include logic operators (e.g. `col1 = 'yellow'`)
        updates (dict[str, str  |  int  |  float]): dictionary of {`column: new_data`, ...} key/value pairs
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        bool: `True` if successful else `False`
    """
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
        print(f"ERROR: {e}")
        return False


# DELETE functions
@connect_to_db
def delete_row(table_name: str, criteria: dict[str, str], db_path: str = "data/capitals.db") -> bool:
    """Deletes a row from a database table

    Args:
        table_name (str): table to be deleted from
        criteria (dict[str, str]): SQL string for search criteria. may include logic operators (e.g. `col1 = 'yellow'`)
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        bool: `True` if successful else `False`
    """
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
        print(f"ERROR: {e}")
        return False


@connect_to_db
def drop_table(table_name: str, db_path: str = "data/capitals.db") -> bool:
    """Removes a table from a database

    Args:
        table_name (str): table to be dropped
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Returns:
        bool: `True` if successful else `False`
    """
    try:
        c.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
        return True
    except sq.OperationalError as e:
        print(f"ERROR: {e}")
        return False


# LOAD functions
def datetime_to_string(serial_date: pd.Timestamp) -> str:
    """Used for converting player birthdays from `timestamp` to formatted string

    Args:
        serial_date (pd.Timestamp): timestamp to be converted

    Returns:
        str: returns date in `mmm dd, yyyy` formatted string
    """
    year = serial_date.year
    month = serial_date.month_name()
    day = serial_date.day
    return f"{month[:3]} {day}, {year}"


@connect_to_db
def load_file(file_to_load: str, table_name: str, drop_columns: list[str], write_type: str = "replace", db_path: str = "data/capitals.db") -> None:
    """Loads a `.xlsx` or `.csv` file into a database table

    Args:
        file_to_load (str): file to be loaded (e.g. `to_load/roster.xlsx`)
        table_name (str): table to add data to. will be created if not exists
        drop_columns (list[str]): list of columns to be dropped before table insertion. use empty list (`[]`) if no columns should be dropped
        write_type (str, optional): _description_. Defaults to "replace".
        db_path (str, optional): `[path]/[filename].db`. Defaults to "data/capitals.db".

    Raises:
        FileTypeError: raised when trying to use a file format other than `.xlsx` or `.csv`
    """
    # read the file
    try:
        if file_to_load.endswith(".xlsx"):
            df = pd.read_excel(file_to_load)
        elif file_to_load.endswith(".csv"):
            df = pd.read_csv(file_to_load)
        else:
            raise FileTypeError([".xlsx", ".csv"])
    except FileTypeError as e:
        print(f"ERROR: {e}")
        return
    except Exception as e:
        print(f"ERROR: {e}")
        return

    # drop columns
    if isinstance(drop_columns, list) and len(drop_columns) >= 1:
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
