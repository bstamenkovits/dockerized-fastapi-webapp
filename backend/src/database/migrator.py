import hashlib
from pathlib import Path
from database.connection import DatabaseConnection


class SQLMigrator:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.db = DatabaseConnection(db_url)
        self.migrations = Path(__file__).parent / "migrations"
        self.ensure_migration_table()

    @staticmethod
    def get_file_hash(filepath: Path) -> str:
        """Get md5 hash of SQL file to detect changes"""
        return hashlib.md5(filepath.read_text().encode()).hexdigest()

    def ensure_migration_table(self):
        """Create table to track applied migrations"""
        query = """
            CREATE TABLE IF NOT EXISTS _migrations (
                file_name TEXT PRIMARY KEY,
                file_hash TEXT NOT NULL,
                applied_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.db.execute_query(query=query)

    def run_migrations(self):
        """Auto-apply SQL schema files"""
        for sql_file in sorted(self.migrations.glob("*.sql")):
            current_hash = self.get_file_hash(sql_file)
            file_name = sql_file.name

            # check if already applied
            result = self.db.fetch_results(
                query="SELECT file_hash FROM _migrations WHERE file_name = ?",
                params=(file_name,)
            )

            # Apply if new or changed
            # TODO: maybe don't allow changes to already applied migrations? Raise error instead of re-applying? Depends on use case.
            if len(result) == 0 or result[0]['file_hash'] != current_hash:
                print(f"Applying schema: {file_name}")
                # use pathlib to read SQL file text (query)
                sql = sql_file.read_text()

                with self.db.get_cursor() as cursor:
                    # execute migration query
                    cursor.execute(sql)

                    # upsert migration record with current hash and timestamp
                    # TODO: same as above todo: maybe don't allow changes to already applied migrations? Raise error instead of re-applying? Depends on use case.
                    cursor.execute(
                        """
                            INSERT INTO _migrations (file_name, file_hash)
                            VALUES (?, ?)
                            ON CONFLICT (file_name)
                            DO UPDATE SET
                                file_hash = EXCLUDED.file_hash,
                                applied_at = CURRENT_TIMESTAMP
                        """,
                        (file_name, current_hash)
                    )
                print(f"✓ Applied: {file_name}")
            else:
                print(f"⊘ Skipped (unchanged): {file_name}")
