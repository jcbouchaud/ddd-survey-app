import functools
import logging

from fastapi import HTTPException

from app.domain.exceptions.template import TemplateNotFoundError

logger = logging.getLogger(__name__)


def handle_exceptions(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except TemplateNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.exception("Unexpected error while creating template", exc_info=e)
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper
