import sqlalchemy

DB_NAME = "clinic_care"
DB_USER = "postgres"
DB_PASS = "asdfasdf"
DB_HOST = "localhost"
DB_PORT = "5432"

database_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = sqlalchemy.create_engine(database_url)