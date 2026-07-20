DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "banking_db"
DB_USER = "admin"
DB_PASSWORD = "password123"

JDBC_URL   = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
JDBC_DRIVER = "org.postgresql.Driver"
JAR_PATH = "/opt/airflow/jars/postgresql-42.7.7.jar"