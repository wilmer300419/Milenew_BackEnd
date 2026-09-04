from decouple import config
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    """Database connection manager class."""

    @staticmethod
    def get_db_connection():
        """
        Static method to establish and return a PostgreSQL database connection.
        Uses RealDictCursor to return query results as dictionary objects.
        """
        try:
            connection = psycopg2.connect(
                host=config('POSTGRES_HOST'),
                user=config('POSTGRES_USER'),
                password=config('POSTGRES_PASSWORD'),
                dbname=config('POSTGRES_DB'),
                port=config('POSTGRES_PORT', default=5432, cast=int),
                cursor_factory=RealDictCursor  # Returns results as dictionaries (JSON-friendly)
            )
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None