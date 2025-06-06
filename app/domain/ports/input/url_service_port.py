from abc import ABC, abstractmethod
from fastapi.responses import JSONResponse

class URLServicePort(ABC):
    
    @abstractmethod
    @classmethod
    def shorten_raw_url(raw_url: str) -> str:
        pass
    
    @abstractmethod
    def save_url(shortened_url: str, raw_url: str) -> JSONResponse:
        pass
    
    @abstractmethod
    def get_url_and_redirect(shortened_url: str) -> JSONResponse:
        pass