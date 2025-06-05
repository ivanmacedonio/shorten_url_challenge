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

# Token management
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_EXPIRATION_TIME = os.getenv("JWT_EXPIRATION_TIME")
