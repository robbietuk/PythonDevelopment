from functools import lru_cache


@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)

if __name__ == "__main__":
    print(f"Fibonacci of 10: {fibonacci(10)}")
    print(f"Fibonacci of 20: {fibonacci(20)}")
    print(f"Fibonacci of 30: {fibonacci(30)}")