import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


class DatabaseConnection:
    """
    A class to manage SQLite database connections and operations.
    """

    def __init__(self, db_path: str | Path = "database.db", enable_column_access_by_name: bool = True):
        """Initialize SQLite database connection."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.enable_column_access_by_name = enable_column_access_by_name

    @contextmanager
    def get_connection(self):
        """Context manager for database connections with auto-commit"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            if self.enable_column_access_by_name:
                connection.row_factory = sqlite3.Row   # Enable column access by name (e.g. row['column_name'])
            yield connection
            connection.commit()  # Auto-commit on successful operations
        except Exception as e:
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Context manager for database connections"""
        with self.get_connection() as conn:
            yield conn.cursor()

    def execute_query(self, query: str, params=None):
        """
        Execute a query that modifies the database (INSERT, UPDATE, DELETE)

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query.

        Returns:
            (int): Number of affected rows.

        Example:
            ```python
            db = DatabaseConnection("mydb.db")
            db.execute_query(
                query="INSERT INTO users (name, age) VALUES (?, ?)",
                params=("Alice", 30)
            )
            ```
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor.rowcount

    def execute_many(self, query: str, params_list):
        """
        Execute a query multiple times with different parameters

        Args:
            query (str): The SQL query to execute.
            params_list (list of tuple): List of parameter tuples to bind to the query.

        Returns:
            (int): Number of affected rows.

        Example:
            ```python
            db = DatabaseConnection("mydb.db")
            db.execute_many(
                query="INSERT INTO users (name, age) VALUES (?, ?)",
                params_list=[
                    ("Alice", 30),
                    ("Bob", 25),
                    ("Charlie", 35)
                ]
            )
            ```
        """
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount

    def fetch_results(self, query: str, params=None):
        """Fetch all results from a SELECT query"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def fetch_one(self, query: str, params=None):
        """Fetch a single result from a SELECT query"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor.fetchone()
