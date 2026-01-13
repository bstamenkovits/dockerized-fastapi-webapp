from database.connection import DatabaseConnection
import config

config.load_environment_variables()

db_path = config.os.getenv("DATABASE_PATH")
db = DatabaseConnection(db_path)

results = db.fetch_results(
    query="SELECT * FROM _migrations"
)

print(results)
print(type(results))
