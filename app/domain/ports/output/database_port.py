from abc import abstractmethod, ABC

class SQLDatabase(ABC):
    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def session_scope_context(self):
        pass
