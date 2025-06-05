from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.domain.configs.dependencies import DATABASE_CONNECT_STRING
from app.domain.ports.output.database_port import SQLDatabase

class DatabaseService(SQLDatabase):
    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._engine = create_engine(DATABASE_CONNECT_STRING, pool_pre_ping=True)
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
        return cls._instance

    def get_session(self):
        return self._SessionLocal()

    @contextmanager
    def session_scope_context(self):
        session = self.get_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

