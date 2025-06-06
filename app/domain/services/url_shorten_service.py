from uuid import UUID
from pydantic import AnyHttpUrl
from fastapi import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.domain.ports.input.url_service_port import URLServicePort
from app.domain.ports.output.repositories.url_repository_port import URLRepositoryPort
from app.domain.entities.url import URLCreateDTO
from app.domain.configs.logging import logger
from app.domain.utils.base62_encoder import generate_random_short_id

class URLShortenService(URLServicePort):
    def __init__(self, repository: URLRepositoryPort):
        self.repository = repository
    
    def get_url_and_redirect(self, shortened_url: str) -> RedirectResponse:
        db_url = self.repository.get_one(shortened_url=shortened_url)
        if not db_url:
            raise HTTPException(status_code=404, detail={"message": f'URL {shortened_url} not found'})
        
        return RedirectResponse(url=db_url.raw_url, status_code=307)
    
    def get_all(self) -> JSONResponse:
        db_urls_list = self.repository.get_all()
        return JSONResponse(
            status_code=200,
            content= {"results": [url.to_dict() for url in db_urls_list]}
        )
    
    def save_url(self, payload: URLCreateDTO, current_user_id: UUID) -> JSONResponse:
        shortened_url = generate_random_short_id()
        shortened_url_already_exists = self.repository.get_one(shortened_url=shortened_url)
        if shortened_url_already_exists: 
            raise HTTPException(
                status_code=400,
                detail={"message": f'shortened url with shortenID: {shortened_url} already exists'}
            )

        commited_shortened_url = self.repository.create(payload=payload,
                                                        current_user_id=current_user_id,
                                                        shortened_url=shortened_url)
        
        logger.info(f'URL shortened with the next ID: {shortened_url}')
        return JSONResponse(
            status_code=201,
            content={
                "message": "URL shortened successfully",
                "shortened_url": commited_shortened_url.shortened_url,
                "original_url": str(payload.raw_url)
            }
        )
    
    def delete(self, shortened_id: str) -> JSONResponse:
        if not shortened_id:
            raise HTTPException(
                status_code=400,
                detail="shortened_id is required"
            )
        updated_url = self.repository.delete_by_shortened_url(shortened_url=shortened_id)
        if not updated_url:
            raise HTTPException(
                status_code=400,
                detail=f'URL with shortened ID {shortened_id} not found or was already deleted'
            )
        
        return JSONResponse(status_code=200, content={"message": f'URL with shortenedID {shortened_id} deleted successfully'})

        
        
    