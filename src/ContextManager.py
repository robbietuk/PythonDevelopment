from collections.abc import Generator
from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timer() -> Generator[None, None, None]:
    start: float = perf_counter()

    try:
        yield
    finally:
        duration: float = perf_counter() - start
        print(f"Elapsed: {duration:.4f}s")


with timer():
    sum(range(10_000_000))