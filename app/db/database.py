import sqlite3
from ..config import SQLITE_DB_PATH, SQLITE_DB_TABLE


class Database:
    def __init__(self, path: str = SQLITE_DB_PATH, table: str = SQLITE_DB_TABLE):
        self.path = path
        self.table = table
        self.conn = None

    def _connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.path)

    def _close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def get_data_by_long_url(self, long_url: str):
        self._connect()
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table} WHERE long_url = ?", (long_url,))
        row = cursor.fetchall()
        return row

    def get_data_by_short_url(self, short_url: str):
        self._connect()
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table} WHERE short_url = ?", (short_url,))
        row = cursor.fetchall()
        return row

    def insert_new_entry(self, entry: dict):
        self._connect()
        cursor = self.conn.cursor()
        cursor.execute(
            f"INSERT INTO {self.table} (id, long_url, short_url) VALUES (?, ?, ?)",
            (
                entry["id"],
                entry["long_url"],
                entry["short_url"],
            ),
        )
        self.conn.commit()

    def get_data(self):
        self._connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM my_table")
        rows = cursor.fetchall()
        return rows

    def set_data(self, data):
        self._connect()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO my_table (name, value) VALUES (?, ?)", data)
        self.conn.commit()

    def __del__(self):
        self._close()
