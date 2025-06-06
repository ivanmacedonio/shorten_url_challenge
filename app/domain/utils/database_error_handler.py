from sqlalchemy.exc import OperationalError, SQLAlchemyError, TimeoutError
from functools import wraps
from fastapi import HTTPException
from app.domain.configs.logging import logger

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except OperationalError as e:
            logger.error(f'Database operation Error: {str(e)}')
            raise HTTPException(
                status_code=500,
                detail={"message": "Database internal error, please contact support", "detail": str(e)})
            
        except SQLAlchemyError as e:
            logger.error(f'ORM unexpected error: {str(e)}')
            raise HTTPException(
                status_code=500,
                detail={"message": "ORM internal error", "detail": str(e)})
            
        except TimeoutError as e:
            logger.error(f'Timeout unexpected error: {str(e)}')
            raise HTTPException(
                status_code=500,
                detail={"message": "Timeout internal error", "detail": str(e)})
    
    return wrapper