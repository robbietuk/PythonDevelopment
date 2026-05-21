from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import Any


def timing_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start: float = perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            duration: float = perf_counter() - start
            print(f"{func.__name__} took {duration:.4f}s")

    return wrapper


@timing_decorator
def calculate_function() -> int:
    return sum(range(1_000_000))

print(calculate_function())
