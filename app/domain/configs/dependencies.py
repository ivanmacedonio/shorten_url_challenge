import os
from dotenv import load_dotenv

load_dotenv(override=True)

# SQL Database
driver = os.getenv("DATABASE_DRIVER", "postgresql")
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST", "localhost")
port = os.getenv("DATABASE_PORT", "5432")
database = os.getenv("DATABASE_NAME")
DATABASE_CONNECT_STRING = f"{driver}://{username}:{password}@{host}:{port}/{database}"
