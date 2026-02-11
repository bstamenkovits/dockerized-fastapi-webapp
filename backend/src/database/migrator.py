import hashlib
import logging
from pathlib import Path
from database.connection import DatabaseConnection

logger = logging.getLogger(__name__)


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

    def apply_migration(self, query, file_name, current_hash: str):
        with self.db.get_cursor() as cursor:
            try:
                cursor.execute(query)
                cursor.execute(
                    """
                        INSERT INTO _migrations (file_name, file_hash)
                        VALUES (?, ?)
                        ON CONFLICT (file_name) DO NOTHING
                    """,
                    (file_name, current_hash)
                )
            except Exception:
                cursor.connection.rollback()
                raise

    def run_migrations(self):
        """Auto-apply SQL schema files"""
        logger.info("Starting SQL migrations...")
        for sql_file in sorted(self.migrations.glob("*.sql")):
            logger.info(f"Processing migration: {sql_file.name}")
            current_hash = self.get_file_hash(sql_file)
            file_name = sql_file.name

            # check if already applied
            result = self.db.fetch_results(
                query="SELECT file_hash FROM _migrations WHERE file_name = ?",
                params=(file_name,)
            )

            # TODO: implement forward-only migrations with version numbers
            if len(result) == 0:
                logger.info(f"Migration {file_name} not found in database. Applying new migration.")
                query = sql_file.read_text()
                try:
                    self.apply_migration(query, file_name, current_hash)
                except Exception as e:
                    logger.exception(f"Failed to apply migration {file_name}")
                    raise
                logger.info(f"✓ Successfully applied: {file_name}")

            elif result[0]['file_hash'] != current_hash:
                logger.error(error_msg := f"Migration {file_name} has changed since it was last applied. Detected hash: {current_hash}, expected hash: {result[0]['file_hash']}.")
                raise Exception(error_msg)

            else:
                logger.info(f"⊘ Skipped (unchanged): {file_name}")
