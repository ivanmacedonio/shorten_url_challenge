from typing import List
from app.domain.ports.output.database_port import SQLDatabase
from app.domain.ports.output.repositories.url_repository_port import URLRepositoryPort
from app.domain.utils.singleton_wrapper import singleton_wrapper
from app.domain.entities.url import URLCreateDTO, URLPartialRetrieveDTO, URLRetrieveDTO
from app.domain.models.models import URL
from app.domain.configs.logging import logger
from app.domain.utils.database_error_handler import handle_db_errors

@singleton_wrapper
class URLRepositoryAdapter(URLRepositoryPort):
    def __init__(self, db_service: SQLDatabase):
        self.db_service = db_service
    
    @handle_db_errors
    def get(self, shortened_url: str) -> URLRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            db_url: URL = session.query(URL).filter_by(shorten_url=shortened_url).first()
            return URLRetrieveDTO(
                id=db_url.id,
                raw_url=db_url.raw_url,
                shorten_url=db_url.shorten_url,
                created_by=db_url.created_by,
                created_at=db_url.created_at,
                deleted=db_url.deleted
            )
    
    @handle_db_errors
    def get_all(self) -> List[URLPartialRetrieveDTO]:
        with self.db_service.session_scope_context() as session:
            db_url_list: List[URL] = session.query(URL).filter_by(deleted=False)
            return [URLPartialRetrieveDTO(
                id=item.id, 
                shorten_url=item.shorten_url
                ) for item in db_url_list]
          
    @handle_db_errors  
    def create(self, payload: URLCreateDTO) -> URLPartialRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            logger.info(f'Creating shortened URL with the next payload: {payload.to_dict()}')
            db_url = URL(raw_url=payload.raw_url, 
                         shorten_url=payload.shorten_url,
                         created_by=payload.created_by)
            session.add(db_url)
            logger.info(f'URL with ID {db_url.id} created successfully')
            session.flush()
            
            return URLPartialRetrieveDTO(
                id=db_url.id,
                shorten_url=db_url.shorten_url
            )
    
    @handle_db_errors
    def delete(self, shortened_url: str) -> URLPartialRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            db_url: URL = session.query(URL).filter_by(shorten_url=shortened_url).first()
            if not db_url: return
            
            db_url.deleted = True
            logger.info(f'URL with ID {db_url.id} soft deleted successfully')
            return URLPartialRetrieveDTO(
                id=db_url.id,
                shorten_url=db_url.shorten_url
            )
        
        
