import asyncio
import bcrypt
from dotenv import dotenv_values
from sqlalchemy.exc import OperationalError
from typing import TypeVar, Callable, Awaitable
from app.utils.logging_config import logger


env = dotenv_values(".env")


async def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


_R = TypeVar("_R")
async def retry_query_on_error(
    query_func: Callable[[], Awaitable[_R]], retries: int = 3, delay: int = 2
) -> _R:
    for attempt in range(retries):
        try:
            return await query_func()
        except OperationalError as e:
            logger.warning(
                "Operational error on attempt '%s': %s", attempt + 1, e, exc_info=True
            )
            if attempt < retries - 1:
                delay_seconds = delay * (2**attempt)
                await asyncio.sleep(delay_seconds)
            else:
                raise
        except Exception as e:
            logger.error(
                "Unexpected error during query execution: %s", e, exc_info=True
            )
            raise
    # This line should be unreachable, but satisfies the type checker:
    raise RuntimeError("retry_query_on_error: reached unreachable code")
