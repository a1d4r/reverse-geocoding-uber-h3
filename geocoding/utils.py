from typing import Any, Callable, TypeVar, cast

import time
from functools import wraps

from loguru import logger

F = TypeVar("F", bound=Callable[..., Any])


def timeit(func: F) -> F:
    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("Function '{}' executed in {:.4f} s", func.__name__, end - start)
        return result

    return cast(F, wrapped)
