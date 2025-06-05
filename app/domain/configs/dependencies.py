import os
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_DEPENDENCIES = {
    "driver": os.getenv("DATABASE_DRIVER", "postgresql"),
    "username": os.getenv("DATABASE_USERNAME"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", 5432)),
    "database": os.getenv("DATABASE_NAME"),
}

DATABASE_CONNECT_STRING = (
    f"{DATABASE_DEPENDENCIES['driver']}://"
    f"{DATABASE_DEPENDENCIES['username']}:{DATABASE_DEPENDENCIES['password']}@"
    f"{DATABASE_DEPENDENCIES['host']}:{DATABASE_DEPENDENCIES['port']}/"
    f"{DATABASE_DEPENDENCIES['database']}"
)
