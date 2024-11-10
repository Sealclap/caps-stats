import sqlite3 as sq

conn = None
c = None


def connect_to_db(func):
    def wrap(*args, **kwargs):
        global conn, c
        conn = sq.connect("data/capitals.db")
        c = conn.cursor()
        result = func(*args, **kwargs)
        conn.close()

        return result
    return wrap


@connect_to_db
def create_tables():
    c.execute("""CREATE TABLE IF NOT EXISTS roster
          (jersey integer primary key,
          name text,
          position text,
          shoots_catches text,
          height text,
          weight integer,
          bday text,
          bplace text)""")


# GET functions
@connect_to_db
def fetch_one(table_name: str, criteria: str) -> tuple | None:
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name} WHERE {criteria}")
        row = c.fetchone()
        return row
    except sq.OperationalError as e:
        print(e)


@connect_to_db
def fetch_many(table_name: str, criteria: str, num_rows: int) -> list[tuple] | None:
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name} WHERE {criteria}")
        rows = c.fetchmany(num_rows)
        return rows
    except sq.OperationalError as e:
        print(e)


@connect_to_db
def fetch_all(table_name: str) -> list[tuple] | None:
    try:
        table_name = table_name.lower()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        return rows
    except sq.OperationalError as e:
        print(e)


# INSERT functions
@connect_to_db
def insert_row(table_name: str, row_data: tuple) -> bool:
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
def insert_rows(table_name: str, num_columns: int, rows_data: list[tuple]) -> bool:
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
def update_row(table_name: str, criteria: str, updates: dict[str, str | int | float]) -> bool:
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
def delete_row(table_name: str, criteria: dict[str, str]) -> bool:
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


create_tables()

if __name__ == '__main__':
    ...
