from typing import List
from uuid import UUID
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
    def get_one(self, shortened_url: str) -> URLRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            db_url: URL = session.query(URL).filter_by(shorten_url=shortened_url, deleted=False).first()
            if not db_url: return 
            
            return URLRetrieveDTO(
                id=db_url.id,
                raw_url=db_url.raw_url,
                shortened_url=db_url.shorten_url,
                created_by=db_url.created_by,
                created_at=db_url.created_at,
                deleted=db_url.deleted
            )
    
    @handle_db_errors
    def get_all(self) -> List[URLRetrieveDTO]:
        with self.db_service.session_scope_context() as session:
            db_url_list: List[URL] = session.query(URL).filter_by(deleted=False)
            return [URLRetrieveDTO(
                shortened_url=item.shorten_url,
                raw_url=item.raw_url,
                created_at=item.created_at,
                created_by=item.created_by,
                deleted=item.deleted
                ) for item in db_url_list]
          
    @handle_db_errors  
    def create(self, payload: URLCreateDTO, current_user_id: UUID, shortened_url: str) -> URLPartialRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            logger.info(f'Creating shortened URL with the next payload: {payload}')
            db_url = URL(raw_url=str(payload.raw_url), 
                         shorten_url=shortened_url,
                         created_by=current_user_id)
            session.add(db_url)
            logger.info(f'URL with ID {db_url.id} created successfully')
            session.flush()
            
            return URLPartialRetrieveDTO(
                id=db_url.id,
                shortened_url=db_url.shorten_url
            )
    
    @handle_db_errors
    def delete_by_shortened_url(self, shortened_url: str) -> URLPartialRetrieveDTO:
        with self.db_service.session_scope_context() as session:
            db_url: URL = session.query(URL).filter_by(shorten_url=shortened_url, deleted=False).first()
            if not db_url: return
            
            db_url.deleted = True
            logger.info(f'URL with ID {db_url.id} soft deleted successfully')
            return URLPartialRetrieveDTO(
                id=db_url.id,
                shortened_url=db_url.shorten_url
            )
        
        
