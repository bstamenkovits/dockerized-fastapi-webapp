import os
from pathlib import Path

def load_environment_variables():
    """
    Load environment variables for the application.

    The environment variables should be defined in the docker-compose.yml file.
    If they are not defined there, this script provides default values to ensure
    the application can run locally without additional configuration.
    """

    # app.db in the data directory at the project root
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite:///../../data/app.db")
    db_path = Path(__file__).parent.parent.parent / "data" / "app.db"
    os.environ["DATABASE_PATH"] = os.getenv("DATABASE_PATH", str(db_path))

    # if running locally, default to development environment
    os.environ["ENVIRONMENT"] = os.getenv("ENVIRONMENT", "development")
